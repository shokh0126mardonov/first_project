from django.utils import timezone

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.accounts.permissions import IsAdmin_or_SuperAdmin
from .models import Inquiry
from .serializers import InquirySerializers, InquirySerializersAdmin


class InquiriesViewSets(ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializers

    def get_serializer_class(self):
        if self.action in ["list", "partial_update"]:
            return InquirySerializersAdmin
        return InquirySerializers

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated, IsAdmin_or_SuperAdmin]

        return [permission() for permission in self.permission_classes]

    def perform_update(self, serializer):

        instance = self.get_object()
        new_status = serializer.validated_data.get("status")

        update_data = {}

        if new_status == "viewed" and instance.viewed_at is None:
            update_data["viewed_at"] = timezone.now()

        if new_status == "responded" and instance.responded_at is None:
            update_data["responded_at"] = timezone.now()

        serializer.save(**update_data)
