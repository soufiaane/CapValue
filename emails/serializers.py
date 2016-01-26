from rest_framework import serializers
from authentication.serializers import AccountSerializer
from emails.models import Email


class EmailSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True, required=False)

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(EmailSerializer, self).get_validation_exclusions()
        return exclusions + ['user']

    class Meta:
        model = Email

        fields = ('id', 'user', 'email', 'password', 'seed', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'seed', 'created_at', 'updated_at')
