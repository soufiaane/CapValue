from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
from team.models import Team
from authentication.models import Account
from authentication.serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),

        if self.request.method == 'POST':
            return permissions.AllowAny(),

        return permissions.IsAuthenticated(), IsAccountOwner(),

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            acc = Account.objects.create_user(**serializer.validated_data)
            if request.data['selected_team']:
                team_id = request.data['selected_team']
                try:
                    selected_team = Team.objects.get(pk=team_id)
                    selected_team.members.add(acc)
                except Exception as ex:
                    print(Type(ex))
            return Response(self.serializer_class(instance=acc).data, status=status.HTTP_201_CREATED)
        return Response({
            'status' : 'Bad request',
            'message': 'Account could not be created with received datata'
        }, status=status.HTTP_400_BAD_REQUEST)


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
            'message': 'Username and/or password invalid.'
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permission_classes = permissions.IsAuthenticated,

    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
