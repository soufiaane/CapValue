from rest_framework import permissions, status, generics, viewsets
from rest_framework.response import Response

from isp.models import ISP
from isp.serializers import ISPSerializer
from mail.models import Email
from team.models import Team


class IspViewSet(viewsets.ModelViewSet):
    queryset = ISP.objects.all()
    serializer_class = ISPSerializer


class AccountIspViewSet(viewsets.ViewSet):
    queryset = ISP.objects.prefetch_related('members').all()
    serializer_class = ISPSerializer

    def list(self, request, account_username=None):
        queryset = self.queryset.filter(members__username=account_username)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


# ----------------------------------------------------
class ISPView(generics.ListCreateAPIView):
    queryset = ISP.objects.all()
    serializer_class = ISPSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid():
            serialized.save(user=self.request.user)
            seed = ISP.objects.get(pk=serialized.data['id'])
            for email in request.data['emails']:
                em = Email.objects.create(user=request.user, email=email['email'], password=email['password'])
                em.save()
                seed.emails.add(em.id)
                seed.save()
            serialized = self.serializer_class(instance=seed)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Team could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamISPList(viewsets.GenericViewSet):
    queryset = ISP.objects.select_related('teams').all()
    serializer_class = ISPSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, **kwargs):
        team_id = kwargs['team_id']
        team = Team.objects.get(pk=team_id)
        queryset = team.isp.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
