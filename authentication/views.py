from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status, views, viewsets, filters, generics
from rest_framework.response import Response
from team.models import Team
from authentication.models import Account
from authentication.serializers import AccountSerializer
import django_filters
from django_filters import MethodFilter


class AccountFilter(filters.FilterSet):
    id = django_filters.NumberFilter(name="id", lookup_type='contains')
    username = django_filters.CharFilter(name="username", lookup_type='contains')
    name = django_filters.CharFilter(name="name", lookup_type='contains')
    first_name = django_filters.CharFilter(name="first_name", lookup_type='contains')
    last_name = django_filters.CharFilter(name="last_name", lookup_type='contains')
    teams = MethodFilter(action='teams_filter')
    entity = MethodFilter(action='entity_filter')
    role = MethodFilter(action='role_filter')
    # role = django_filters.CharFilter(name="role", lookup_type='contains')

    def teams_filter(self, queryset, value):
        if hasattr(queryset, 'qs'):
            return queryset.qs.filter(teams=value)
        else:
            return queryset.filter(teams=value)

    def entity_filter(self, queryset, value):
        if hasattr(queryset, 'qs'):
            return queryset.qs.filter(teams__entity=value)
        else:
            return queryset.filter(teams__entity=value)

    def role_filter(self, queryset, value):
        if hasattr(queryset, 'qs'):
            return queryset.qs.filter(groups__name=value)
        else:
            return queryset.filter(groups__name=value)

    # team = django_filters.CharFilter(name="team", lookup_type='contains')

    class Meta:
        model = Account
        fields = ['id', 'username', 'first_name', 'last_name', 'entity', 'teams', 'role']


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
            'status': 'Bad request',
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
                'status': 'Unauthorized',
                'message': 'This account has been disabled.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'status': 'Unauthorized',
            'message': 'Username and/or password invalid.'
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permission_classes = permissions.IsAuthenticated,

    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class AccountProfileViewSet(generics.RetrieveAPIView, views.APIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = permissions.AllowAny,
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AccountFilter
    ordering_fields = ('id', 'username', 'first_name', 'last_name', 'entity', 'teams', 'role')

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering', None)
        filter_id = self.request.query_params.get('id', None)
        username = self.request.query_params.get('username', None)
        first_name = self.request.query_params.get('first_name', None)
        last_name = self.request.query_params.get('last_name', None)
        teams = self.request.query_params.get('team', None)
        entity = self.request.query_params.get('entity', None)
        role = self.request.query_params.get('role', None)
        queryset = self.queryset
        if ordering:
            queryset = self.queryset.order_by(ordering)
        if username:
            if hasattr(queryset, 'qs'):
                queryset = AccountFilter({'username': username}, queryset=queryset.qs)
            else:
                queryset = AccountFilter({'username': username}, queryset=queryset)
        if first_name:
            if hasattr(queryset, 'qs'):
                queryset = AccountFilter({'first_name': first_name}, queryset=queryset.qs)
            else:
                queryset = AccountFilter({'first_name': first_name}, queryset=queryset)
        if last_name:
            if hasattr(queryset, 'qs'):
                queryset = AccountFilter({'last_name': last_name}, queryset=queryset.qs)
            else:
                queryset = AccountFilter({'last_name': last_name}, queryset=queryset)
        if filter_id:
            if hasattr(queryset, 'qs'):
                queryset = AccountFilter({'id': filter_id}, queryset=queryset.qs)
            else:
                queryset = AccountFilter({'id': filter_id}, queryset=queryset)
        if entity:
            if hasattr(queryset, 'qs'):
                queryset = AccountFilter({'entity': entity}, queryset=queryset.qs)
            else:
                queryset = AccountFilter({'entity': entity}, queryset=queryset)
        if teams:
            if hasattr(queryset, 'qs'):
                queryset = AccountFilter({'teams': teams}, queryset=queryset.qs)
            else:
                queryset = AccountFilter({'teams': teams}, queryset=queryset)

        if role:
            if hasattr(queryset, 'qs'):
                queryset = AccountFilter({'role': role}, queryset=queryset.qs)
            else:
                queryset = AccountFilter({'role': role}, queryset=queryset)
        if hasattr(queryset, 'qs'):
            return queryset.qs
        return queryset

    def get(self, request, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
