from rest_framework import permissions, status, views, generics
from django.contrib.auth import authenticate, login, logout
from authentication.serializers import AccountSerializer
from rest_framework.response import Response
from authentication.models import Account
from team.models import Team


class AccountView(generics.ListCreateAPIView):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid():
            Account.objects.create_user(**serialized.validated_data)
            return Response(serialized.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status' : 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'Manager':
            queryset = self.filter_queryset(self.get_queryset())
        elif user.role == 'Team Leader':
            user_team = Team.objects.get(team_leader=user)
            queryset = user_team.team_members.all()
        else:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(views.APIView):
    def post(self, request, format=None):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = AccountSerializer(account)

                return Response(serialized.data)

            return Response({
                'status' : 'Unauthorized',
                'message': 'This account has been disabled.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'status' : 'Unauthorized',
            'message': 'Username/password combination invalid.'
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
