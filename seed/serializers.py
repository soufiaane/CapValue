from rest_framework import serializers
from seed.models import Seed
from authentication.serializers import AccountSerializer

class SeedSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True, required=False)
    class Meta:
        model = Seed

        fields = ('id', 'user', 'jobs', 'list_name', 'proxyType', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'jobs', 'created_at', 'updated_at')

        def get_validation_exclusions(self, *args, **kwargs):
            exclusions = super(SeedSerializer, self).get_validation_exclusions()

            return exclusions + ['user']
