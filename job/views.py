from rest_framework import viewsets, permissions, generics, status, views
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from mail.serializers import EmailSerializer
from seed.serializers import SeedSerializer
from celeryTasks.celerySettings import app
from proxy.serializers import IPSerializer
from job.serializers import JobSerializer
from celery.result import GroupResult
from django.utils.six import BytesIO
from tasks import report_hotmail
from mail.models import Email
from job.models import Seed
from job.models import Job
from celery import group
import signal
import json


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def create(self, request, *args, **kwargs):
        subject = request.data.get('keywords', None)
        actions = request.data.get('actions', None)
        wait_timeout = int(request.data.get('wait_timeout', None))
        hide_browser = bool(request.data.get('hide_browser', False))
        cc = str(request.data.get('concurrency', 1))
        user = request.user
        qq = user.username + cc

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
            report_hotmail.s(actions=actions, subject=subject, email=emm[i], proxy=pr[i], wait_timeout=wait_timeout,
                             hide_browser=hide_browser).set(queue=qq) for i in range(len(emm)))
        tas_results = tas.apply_async()
        tas_results.save()
        job.celery_id = tas_results.id
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


class RevokeJob(views.APIView):
    permission_classes = permissions.IsAuthenticated,

    def post(self, request, format=None):
        group_id = request.data.get('celery_id', None)
        if group_id:
            app.control.revoke([task.id for task in GroupResult.restore(group_id)], terminate=True,
                               signal=signal.SIGILL)
            return Response(status=status.HTTP_200_OK)

        return Response({
            'status': 'Bad request',
            'message': 'Job could not be stopped with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateJobResults(views.APIView):
    permission_classes = permissions.IsAuthenticated,
    serializer_class = JobSerializer

    def post(self, request, format=None):
        model_jobs = []
        req_jobs = request.data.get('jobs', None)
        for req_job in req_jobs:
            job = Job.objects.get(pk=req_job['id'])
            results = GroupResult.restore(id=job.celery_id)
            print("Successful: %s\n" % results.successful())
            print("ready: %s\n" % results.ready())
            print("completed count: %s\n" % results.completed_count())

        group_id = request.data.get('celery_id', None)
        if group_id:
            app.control.revoke([task.id for task in GroupResult.restore(group_id)], terminate=True,
                               signal=signal.SIGILL)
            return Response(status=status.HTTP_200_OK)

        return Response({
            'status': 'Bad request',
            'message': 'Job could not be stopped with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)
