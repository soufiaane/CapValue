from rest_framework import serializers

from proxy.models import IP, Proxy


class IPSerializer(serializers.ModelSerializer):
    proxy_name = serializers.SlugRelatedField(many=True, read_only=True, slug_field="proxy_name", source="proxies")

    class Meta:
        model = IP
        fields = (
            'id', 'ip_address', 'proxies', 'proxy_name', 'ip_port', 'ip_login', 'ip_password', 'created_at',
            'updated_at')
        read_only_fields = ('id', 'proxies', 'proxy_name', 'created_at', 'updated_at')


class ProxySerializer(serializers.ModelSerializer):
    class Meta:
        model = Proxy
        fields = ('id', 'proxy_name', 'proxy_type', 'created_at', 'updated_at')
        read_only_fields = ('id', 'owner', 'ip_list', 'created_at', 'updated_at')
