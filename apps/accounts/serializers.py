from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "groups",
            "user_permissions",
            "is_staff",
            "is_superuser",
            "last_login",
            "password",
            "role",
            "date_joined",
            "is_active",
        ]


class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
