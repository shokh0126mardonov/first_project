from django.utils import timezone
from rest_framework import serializers

from .models import Inquiry


# class InquirySerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Inquiry
#         fields = '__all__'


class InquirySerializers(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ["id", "full_name", "phone", "email", "message", "product"]

    def get_product_name(self, obj):
        if obj.product:
            return obj.product.name
        return None


class InquirySerializersAdmin(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = "__all__"

    def update(self, instance, validated_data):

        new_status = validated_data.get("status")

        if new_status == "viewed":
            validated_data["viewed_at"] = timezone.now()

        if new_status == "responded":
            validated_data["responded_at"] = timezone.now()

        return super().update(instance, validated_data)
