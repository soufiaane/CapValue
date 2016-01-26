from rest_framework import serializers
from isp.models import ISP


class ISPSerializer(serializers.ModelSerializer):
    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(ISPSerializer, self).get_validation_exclusions()
        return exclusions + ['teams']

    class Meta:
        model = ISP
        fields = ('id', 'isp_name', 'teams', 'created_at', 'updated_at')
        read_only_fields = ('id', 'teams', 'created_at', 'updated_at')
