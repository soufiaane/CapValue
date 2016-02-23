from rest_framework import viewsets, permissions, generics, status
from proxies.serializers import ProxySerializer, IPSerializer
from rest_framework.response import Response
from proxies.models import Proxy, IP


class ProxyView(generics.ListCreateAPIView):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        proxy = Proxy.objects.create(user=self.request.user, proxy_name=data["proxy_name"], proxy_type=data["proxy_type"])
        proxy.save()
        for ip in data["ips"]:
            iip = IP.objects.create(ip_address=ip["ip"], ip_port=ip["port"], ip_login=ip["login"], ip_password=ip["pass"])
            iip.save()
            proxy.ip_list.add(iip)
            proxy.save()
        serializer = self.get_serializer(proxy)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IPViewSet(viewsets.ModelViewSet):
    queryset = IP.objects.all()
    serializer_class = IPSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
