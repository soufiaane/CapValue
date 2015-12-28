from rest_framework import serializers
from job.models import Job
from authentication.serializers import AccountSerializer
from seed.serializers import SeedSerializer


class JobSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True, required=False)
    # seed_list = SeedSerializer(read_only=True, required=False)

    class Meta:
        model = Job
        fields = ('user', 'entered', 'finished',
                  'keyword', 'status', 'processed',
                  'actions',)
        read_only_fields = ('entered', 'finished',)

        def create(self, validated_data):
            return Job.objects.create(**validated_data)
