from rest_framework import viewsets, permissions
from rest_framework.response import Response
from seed.serializers import SeedSerializer
from seed.models import Seed
from seed.permissions import IsOwnerOfSeedList


class SeedViewSet(viewsets.ModelViewSet):
    queryset = Seed.objects.all()
    serializer_class = SeedSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwnerOfSeedList(),)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        return super(SeedViewSet, self).perform_create(serializer)


class AccountSeedViewSet(viewsets.ViewSet):
    queryset = Seed.objects.select_related('user').all()
    serializer_class = SeedSerializer

    def list(self, request, account_username=None):
        queryset = self.queryset.filter(user__username=account_username)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
