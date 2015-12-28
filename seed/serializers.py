from rest_framework import serializers
from job.models import Job


class SeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('jobid', 'user', 'entered', 'finished',
                  'keyword', 'status', 'processed',
                  'actions',)
        read_only_fields = ('entered', 'finished',)

        def create(self, validated_data):
            return Job.objects.create(**validated_data)
