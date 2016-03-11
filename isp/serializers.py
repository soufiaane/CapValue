from rest_framework import serializers

from isp.models import ISP


class ISPSerializer(serializers.ModelSerializer):
    teams = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name", source="teams")

    class Meta:
        model = ISP
        fields = ('id', 'teams', 'name', 'logo', 'created_at', 'updated_at')
        read_only_fields = ('id', 'teams', 'created_at', 'updated_at')
