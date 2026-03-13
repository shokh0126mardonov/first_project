from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.accounts.permissions import IsAdmin_or_SuperAdmin, IsSuperAdmin
from .models import Product
from .serializers import ProductSerializers
from .pagination import CustomPagination
from .filters import ProductFilter

class ProductViewSets(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    pagination_class = CustomPagination
    
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]

    filterset_class = ProductFilter

    ordering_fields = [
        "price",
        "power_watt",
        "created_at",
    ]

    search_fields = [
        "name",
    ]

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action in ["create", "update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsAdmin_or_SuperAdmin]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsSuperAdmin]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Products"])
class ProductViewSets(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializers