from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response

from mail.models import Email
from proxy.models import Proxy, IP
from seed.models import Seed
from seed.serializers import SeedSerializer


class SeedViewSet(viewsets.ModelViewSet):
    queryset = Seed.objects.all()
    serializer_class = SeedSerializer

    def create(self, request, *args, **kwargs):
        seed = Seed.objects.create(owner=request.user, name=request.data['list_name'])
        # , proxy=request.data['proxyType'])
        seed.save()
        proxy = None
        if request.data['proxyType'] == 'manual':
            try:
                proxy = Proxy.objects.get(owner=request.user, proxy_name="Manual")
            except:
                proxy = Proxy.objects.create(owner=request.user, proxy_name="Manual")
                proxy.save()
        for email in request.data['emails']:
            em = Email.objects.create(owner=request.user, login=email['email'], password=email['password'])
            em.save()
            if proxy and email['proxy']:
                if (email['proxy']['ip'] is not '') and (email['proxy']['port'] is not ''):
                    try:
                        ip = IP.objects.create(ip_address=email['proxy']['ip'], ip_port=email['proxy']['ip'],
                                               ip_login=email['proxy']['login'], ip_password=email['proxy']['pass'])
                        ip.save()
                        proxy.ip_list.add(ip)
                        proxy.save()
                        em.proxy.add(proxy)
                    except KeyError:
                        ip = IP.objects.create(ip_address=email['proxy']['ip'], ip_port=email['proxy']['port'])
                        ip.save()
                        proxy.ip_list.add(ip)
                        proxy.save()
                        em.proxy.add(proxy)
            em.save()
            seed.emails.add(em.id)
            seed.save()
        serialized = self.serializer_class(instance=Seed.objects.get(pk=seed.id))
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class AccountSeedViewSet(generics.ListCreateAPIView, viewsets.ViewSet):
    queryset = Seed.objects.prefetch_related('owner').all()
    serializer_class = SeedSerializer
    permission_classes = permissions.AllowAny,

    def list(self, request, account_username=None, **kwargs):
        queryset = self.queryset.filter(owner__username=account_username)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
