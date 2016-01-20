from rest_framework import viewsets, permissions

from proxies.models import Proxy
from proxies.serializers import ProxySerializer


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
