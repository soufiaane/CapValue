from rest_framework import serializers

from team.models import Team


class TeamSerializer(serializers.ModelSerializer):
    entity = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Team
        fields = ('id', 'name', 'logo', 'members', 'entity', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
