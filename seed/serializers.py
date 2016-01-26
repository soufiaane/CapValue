from authentication.serializers import AccountSerializer
from rest_framework import serializers
from seed.models import Seed


class SeedSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True, required=False)

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(SeedSerializer, self).get_validation_exclusions()
        return exclusions + ['emails']

    class Meta:
        model = Seed
        fields = ('id', 'user', 'jobs', 'emails', 'list_name', 'proxyType', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'jobs', 'emails', 'created_at', 'updated_at')
