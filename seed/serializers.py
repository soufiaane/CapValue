from authentication.serializers import AccountSerializer
from emails.serializers import EmailSerializer
from rest_framework import serializers
from seed.models import Seed

class SeedSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True, required=False)
    emails = EmailSerializer(read_only=True, required=False, many=True)

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(SeedSerializer, self).get_validation_exclusions()
        return exclusions + ['emails', 'jobs']

    class Meta:
        model = Seed
        fields = ('id', 'user', 'jobs', 'emails', 'list_name', 'proxyType', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'jobs', 'emails', 'created_at', 'updated_at')
