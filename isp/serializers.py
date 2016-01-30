from rest_framework import serializers
from isp.models import ISP
from team.serializers import TeamSerializer


class ISPSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True)

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(ISPSerializer, self).get_validation_exclusions()
        return exclusions + ['teams']

    class Meta:
        model = ISP
        fields = ('id', 'isp_name', 'teams', 'members', 'logo', 'created_at', 'updated_at')
        read_only_fields = ('id', 'teams', 'members', 'created_at', 'updated_at')
