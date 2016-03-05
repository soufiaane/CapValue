from rest_framework import permissions, status, generics, viewsets
from rest_framework.response import Response

from isp.models import ISP
from mail.models import Email
from team.models import Team
from team.serializers import TeamSerializer


class TeamView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid():
            serialized.save(user=self.request.user)
            seed = Team.objects.get(pk=serialized.data['id'])
            for email in request.data['emails']:
                em = Email.objects.create(user=request.user, email=email['email'], password=email['password'])
                em.save()
                seed.emails.add(em.id)
                seed.save()
            serialized = self.serializer_class(instance=seed)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response({
            'status' : 'Bad request',
            'message': 'Team could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ISPTeamList(viewsets.GenericViewSet):
    queryset = Team.objects.select_related('isp').all()
    serializer_class = TeamSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, **kwargs):
        isp_id = kwargs['isp_id']
        isp = ISP.objects.get(pk=isp_id)
        queryset = isp.teams.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
