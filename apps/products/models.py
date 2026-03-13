from django.db import models
from django.conf import settings


class Product(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products"
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    power_watt = models.PositiveIntegerField()
    efficiency = models.CharField(max_length=50)
    warranty_years = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/%Y/%m/%d/", blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_product"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.pk} {self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )

    image = models.ImageField(upload_to="products/%Y/%m/%d/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
