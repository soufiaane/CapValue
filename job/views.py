from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from job.serializers import JobSerializer
from job.permissions import IsOwnerOfJob
from job.tasks import reportHotmail
from job.models import Job
from job.models import Seed
import json


class JobView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        keywords = request.data.get('keywords', None)
        seed_list = json.loads(request.data.get('seed_list', None))
        actions = request.data.get('actions', None)
        user = request.user
        serialized = self.serializer_class(data={'keywords': keywords, 'actions': actions})
        if serialized.is_valid():
            job = Job.objects.create(keywords=keywords, actions=actions, user=user)
            for seed in seed_list:
                pk = int(seed['id'])
                seed = Seed.objects.get(pk=pk)
                job.seed_list.add(seed)

            seeds = job.seed_list.all()
            for seed in seeds:
                emails = seed.emails.all()
                for email in emails:
                    reportHotmail.delay(reportHotmail, job, email)
            job.status = "RN"
            job.save()

            serialized = self.serializer_class(instance=job)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response({
            'status' : 'Bad request',
            'message': 'Job could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass


class AccountJobList(viewsets.GenericViewSet):
    queryset = Job.objects.select_related('user').all()
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOfJob,)

    def list(self, request, **kwargs):
        username = kwargs.get('username')
        queryset = self.queryset.filter(user__username=username)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
