from rest_framework import viewsets, permissions
from rest_framework.response import Response
from job.serializers import JobSerializer
from job.models import Job
from job.permissions import IsOwnerOfSeedList


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsOwnerOfSeedList(),)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, seed_list=self.request.seed_list)

        return super(JobViewSet, self).perform_create(serializer)


class AccountJobViewSet(viewsets.ViewSet):
    queryset = Job.objects.select_related('user').all()
    serializer_class = JobSerializer

    def list(self, request, account_username=None):
        queryset = self.queryset.filter(user__username=account_username)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
