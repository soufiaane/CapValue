from rest_framework import viewsets, permissions
from rest_framework.response import Response

from seed.models import Seed
from seed.permissions import IsOwnerOfSeedList
from seed.serializers import SeedSerializer


class SeedViewSet(viewsets.ModelViewSet):
    queryset = Seed.objects.all()
    serializer_class = SeedSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOfSeedList,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('categoria', 'categoria__titulo',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super(SeedViewSet, self).perform_create(serializer)


class AccountSeedViewSet(viewsets.ModelViewSet):
    queryset = Seed.objects.select_related('user').all()
    serializer_class = SeedSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOfSeedList,)

    def list(self, request, **kwargs):
        queryset = self.queryset.filter(user__username=kwargs.get('account_username'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
