from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from seed.models import Seed
from seed.serializers import SeedSerializer


class AccountSeedList(viewsets.GenericViewSet):
    queryset = Seed.objects.prefetch_related('owner').all()
    serializer_class = SeedSerializer
    permission_classes = permissions.AllowAny,

    def list(self, **kwargs):
        username = kwargs.get('account_username')
        queryset = self.queryset.filter(owner__username=username)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SeedViewSet(viewsets.ModelViewSet):
    queryset = Seed.objects.all()
    serializer_class = SeedSerializer

# class SeedView(generics.ListCreateAPIView):
#     queryset = Seed.objects.all()
#     serializer_class = SeedSerializer
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         serialized = self.serializer_class(data=request.data)
#         if serialized.is_valid():
#             serialized.save(user=self.request.user)
#             seed = Seed.objects.get(pk=serialized.data['id'])
#             for email in request.data['emails']:
#                 em = Email.objects.create(user=request.user, email=email['email'], password=email['password'])
#                 em.save()
#                 seed.emails.add(em.id)
#                 seed.save()
#             serialized = self.serializer_class(instance=seed)
#             return Response(serialized.data, status=status.HTTP_201_CREATED)
#
#         return Response({
#             'status' : 'Bad request',
#             'message': 'SeedList could not be created with received data.'
#         }, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         # page = self.paginate_queryset(queryset)
#         # if page is not None:
#         #     serializer = self.get_serializer(page, many=True)
#         #     return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class SeedDetail(generics.RetrieveUpdateDestroyAPIView):
#     def get(self, request, *args, **kwargs):
#         print(request)
#
#     def put(self, request, *args, **kwargs):
#         print(request)
#
#     def delete(self, request, *args, **kwargs):
#         print(request)
