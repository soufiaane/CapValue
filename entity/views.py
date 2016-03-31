from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from entity.models import Entity
from entity.serializers import EntitySerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = permissions.AllowAny,
