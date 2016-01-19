from rest_framework import viewsets, permissions
from rest_framework.response import Response

from seed.models import Seed
from seed.permissions import IsOwnerOfSeedList
from seed.serializers import SeedSerializer


class SeedViewSet(viewsets.ModelViewSet):
    queryset = Seed.objects.all()
    serializer_class = SeedSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOfSeedList,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super(SeedViewSet, self).perform_create(serializer)


class AccountSeedList(viewsets.GenericViewSet):
    queryset = Seed.objects.select_related('user').all()
    serializer_class = SeedSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOfSeedList,)

    def list(self, request, **kwargs):
        username = kwargs.get('username')
        queryset = self.queryset.filter(user__username=username)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
