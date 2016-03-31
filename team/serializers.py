from rest_framework import serializers

from team.models import Team


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name', 'members', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
