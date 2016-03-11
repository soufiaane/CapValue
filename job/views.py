import json

from celery import group
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response

from job.models import Job
from job.models import Seed
from job.serializers import JobSerializer
from mail.models import Email
from mail.serializers import EmailSerializer
from proxy.serializers import IPSerializer
from seed.serializers import SeedSerializer
from tasks import report_hotmail


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def create(self, request, *args, **kwargs):
        subject = request.data.get('keywords', None)
        actions = request.data.get('actions', None)
        user = request.user
        seed_list = json.loads(request.data.get('seed_list', None))
        job = Job.objects.create(subject=subject, actions=actions, owner=user)
        [job.seeds.add(Seed.objects.get(pk=seed['id'])) for seed in seed_list]

        pr = []
        emm = []
        for seed in seed_list:
            for email_id in seed['emails']:
                current_email = current_proxy = None
                try:
                    current_email = EmailSerializer(Email.objects.get(pk=email_id)).data
                    current_proxy = IPSerializer(
                        instance=Email.objects.get(pk=email_id).proxy.last().ip_list.last()).data
                except AttributeError:
                    pass
                if current_email is not None:
                    emm.append(current_email)
                else:
                    emm.append(None)
                if current_proxy is not None:
                    pr.append(current_proxy)
                else:
                    pr.append(None)
        tas = group(
            report_hotmail.s(actions=actions, subject=subject, email=emm[i], proxy=pr[i]).set(queue=user.username) for i
            in range(len(emm)))()
        job.celery_id = tas.id
        job.status = "RN"
        job.save()
        return Response(self.serializer_class(instance=job).data, status=status.HTTP_201_CREATED)


class AccountJobViewSet(generics.ListCreateAPIView, viewsets.ViewSet):
    queryset = Job.objects.select_related('owner').all()
    serializer_class = JobSerializer
    permission_classes = permissions.AllowAny,

    def list(self, request, account_username=None, **kwargs):
        queryset = self.queryset.filter(owner__username=account_username)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO-CVC remove
class JobView(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        keywords = request.data.get('keywords', None)
        seed_list = json.loads(request.data.get('seed_list', None))
        actions = request.data.get('actions', None)
        user = request.user
        serialized = self.serializer_class(data={'keywords': keywords, 'actions': actions})
        if serialized.is_valid():
            job = Job.objects.create(keywords=keywords, actions=actions, user=user)
            [job.seed_list.add(Seed.objects.get(pk=seed['id'])) for seed in seed_list]
            job.save()
            [seed.jobs.add(job) for seed in job.seed_list.all()]
            job_ser = self.serializer_class(instance=job)
            seed_ser = SeedSerializer(instance=job.seed_list.all(), many=True)
            [[report_hotmail.apply_async((job_ser.data, email), queue='Test') for email in seed['emails']] for seed in
             seed_ser.data]
            job.status = "RN"
            job.save()
            return Response(job_ser.data, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Job could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass
