from rest_framework import serializers

from seed.models import Seed


class SeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seed
        fields = ('id', 'owner', 'emails', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
