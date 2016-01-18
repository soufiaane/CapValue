from rest_framework import viewsets, permissions
from rest_framework.response import Response
from job.serializers import JobSerializer
from job.models import Job
from seed.models import Seed
from job.permissions import IsOwnerOfJob
from job.tasks import reportTask


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOfJob,)

    def perform_create(self, serializer):
        data = self.request.data
        s_list = []
        for seed in data['seed_list']:
            s_list.append(Seed.objects.get(pk=seed['id']).id)
        serializer.save(user=self.request.user, keywords=data['keywords'], actions=data['actions'], seed_list=s_list)
        # reportTask.delay()
        return super(JobViewSet, self).perform_create(serializer)


class AccountJobViewSet(viewsets.ViewSet):
    queryset = Job.objects.select_related('user').all()
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOfJob,)

    def list(self, request, account_username=None):
        queryset = self.queryset.filter(user__username=account_username)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
