from django.db import models

from authentication.models import Account


class IP(models.Model):
    ip_address = models.CharField(max_length=40, blank=True, null=True)
    ip_port = models.IntegerField()
    ip_login = models.CharField(max_length=40, blank=True, null=True)
    ip_password = models.CharField(max_length=40, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s:%s' % ip_address, ip_port


class Proxy(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='proxies', null=True)
    ip_list = models.ManyToManyField(IP, related_name='proxies')
    proxy_name = models.CharField(max_length=40, blank=True)
    proxy_type = models.CharField(max_length=40, blank=True, default='Manual')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % proxy_name
