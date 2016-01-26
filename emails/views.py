from rest_framework import viewsets, permissions, status, generics
from emails.permissions import *
from rest_framework.response import Response
from emails.serializers import EmailSerializer
from emails.models import Email


class EmailView(generics.ListCreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid():
            serialized.save(user=self.request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response({
            'status' : 'Bad request',
            'message': 'Email could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EmailDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        print(request)

    def put(self, request, *args, **kwargs):
        print(request)

    def delete(self, request, *args, **kwargs):
        print(request)


class AccountEmailList(viewsets.GenericViewSet):
    queryset = Email.objects.select_related('user').all()
    serializer_class = EmailSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, **kwargs):
        username = kwargs.get('username')
        queryset = self.queryset.filter(user__username=username)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
