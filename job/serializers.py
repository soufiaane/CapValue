from rest_framework import serializers
from job.models import Job
from authentication.serializers import AccountSerializer
from seed.serializers import SeedSerializer


class JobSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True, required=False)

    class Meta:
        model = Job

        fields = ('id', 'user', 'seed_list', 'keywords', 'actions', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'seed_list', 'created_at', 'updated_at')

        def get_validation_exclusions(self, *args, **kwargs):
            exclusions = super(JobSerializer, self).get_validation_exclusions()
            return exclusions + ['user', 'seed_list']
