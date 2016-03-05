from rest_framework import serializers

from mail.models import Email


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('id', 'owner', 'login', 'password', 'isActive', 'version', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
