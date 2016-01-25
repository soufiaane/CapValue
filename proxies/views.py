from rest_framework import viewsets, permissions

from proxies.models import Proxy, IP
from proxies.serializers import ProxySerializer, IPSerializer


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        data = self.request.data
        s_list = []
        for seed in data['seed_list']:
            s_list.append(Proxy.objects.get(pk=seed['id']).id)
        serializer.save(user=self.request.user, keywords=data['keywords'], actions=data['actions'], seed_list=s_list)
        return super(ProxyViewSet, self).perform_create(serializer)


class IPViewSet(viewsets.ModelViewSet):
    queryset = IP.objects.all()
    serializer_class = IPSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
