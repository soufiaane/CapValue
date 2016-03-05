from rest_framework import serializers

from authentication.serializers import AccountSerializer
from proxy.models import IP, Proxy


class IPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IP
        fields = ('id', 'proxies', 'ip_address', 'ip_port', 'ip_login', 'ip_password', 'created_at', 'updated_at')
        read_only_fields = ('id', 'proxies', 'created_at', 'updated_at')


class ProxySerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True, required=False)

    class Meta:
        model = Proxy
        fields = ('id', 'user', 'ip_list', 'proxy_name', 'proxy_type', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
