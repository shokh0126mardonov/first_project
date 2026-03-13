from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SUPERADMIN = "SUPERADMIN", "Superadmin"

    role = models.CharField(choices=Role.choices, default=Role.ADMIN, max_length=10)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_superadmin(self):
        return self.role == self.Role.SUPERADMIN

    def __str__(self):
        return f"{self.pk} {self.username}"
