from rest_framework import serializers

from apps.accounts.serializers import UserSerializers
from .models import Product


class ProductSerializers(serializers.ModelSerializer):
    created_by = UserSerializers(read_only=True)

    class Meta:
        model = Product
        fields = [
            "pk",
            "created_by",
            "name",
            "description",
            "price",
            "power_watt",
            "efficiency",
            "warranty_years",
            "image",
            "is_active",
            "created_at",
            "updated_at",
        ]
