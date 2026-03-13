from django.db import models
from apps.products.models import Product
from phonenumber_field.modelfields import PhoneNumberField


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("viewed", "Viewed"),
        ("responded", "Responded"),
        ("closed", "Closed"),
    ]

    full_name = models.CharField(max_length=255)

    phone = PhoneNumberField()

    email = models.EmailField(blank=True, null=True)

    message = models.TextField()

    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="inquiries"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    admin_note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    viewed_at = models.DateTimeField(null=True, blank=True)

    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "inquiries_inquiry"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.phone}"
