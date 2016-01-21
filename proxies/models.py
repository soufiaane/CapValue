from datetime import datetime
from django.db import models
from authentication.models import Account


class IP(models.Model):
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    ip_port = models.IntegerField()
    ip_login = models.CharField(max_length=40, blank=True)
    ip_password = models.CharField(max_length=40, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True, default=datetime.now)

    def __unicode__(self):
        return '{0}'.format(self.ip_address)


class Proxy(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    ip_list = models.ManyToManyField(IP, related_name='proxies')
    proxy_name = models.CharField(max_length=40, blank=True)
    proxy_type = models.CharField(max_length=40, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True, default=datetime.now)

    def __unicode__(self):
        return '{0}'.format(self.proxy_name)

