from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from authentication.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    role = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name", source="groups")

    class Meta:
        model = Account
        fields = ("id", "username", "first_name", "last_name", "role", "profile_picture", "created_at", "updated_at", "password", "confirm_password")
        read_only_fields = ("id", "created_at", "updated_at",)

        def update(self, instance, validated_data):
            instance.username = validated_data.get("username", instance.username)
            instance.first_name = validated_data.get("first_name", instance.first_name)
            instance.last_name = validated_data.get("last_name", instance.last_name)

            instance.save()

            password = validated_data.get("password", None)
            confirm_password = validated_data.get("confirm_password", None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get("request"), instance)

            return instance
