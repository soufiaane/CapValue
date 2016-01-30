from authentication.serializers import AccountSerializer
from rest_framework import serializers
from team.models import Team

class TeamSerializer(serializers.ModelSerializer):
    team_leader = AccountSerializer(read_only=True, required=False)
    team_members = AccountSerializer(read_only=True, required=False, many=True)

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(TeamSerializer, self).get_validation_exclusions()
        return exclusions + ['isp', 'team_members']

    class Meta:
        model = Team
        fields = ('id', 'team_name', 'team_leader', 'team_members', 'isp', 'created_at', 'updated_at')
        read_only_fields = ('id', 'team_leader', 'team_members', 'isp', 'created_at', 'updated_at')
