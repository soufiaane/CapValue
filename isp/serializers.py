from rest_framework import serializers

from isp.models import ISP


class ISPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ISP
        fields = ('id', 'name', 'logo', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
