from rest_framework.response import Response
from team.serializers import TeamSerializer
from rest_framework import viewsets
from team.models import Team


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class AccountTeamViewSet(viewsets.ViewSet):
    queryset = Team.objects.prefetch_related('members').all()
    serializer_class = TeamSerializer

    def list(self, request, account_username=None):
        queryset = self.queryset.filter(members__username=account_username)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class EntityTeamViewSet(viewsets.ViewSet):
    queryset = Team.objects.prefetch_related('entity').all()
    serializer_class = TeamSerializer

    def list(self, request, entity_pk=None):
        queryset = self.queryset.filter(entity__id=entity_pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
