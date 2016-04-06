from django.db import models
from authentication.models import Account
from proxy.models import Proxy
from isp.models import ISP


class Email(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="emails", null=True)
    login = models.CharField(max_length=256, blank=True)
    password = models.CharField(max_length=50, blank=True)
    proxy = models.ManyToManyField(Proxy, related_name="emails")
    isActive = models.BooleanField(default=True)
    isp = models.ManyToManyField(ISP, related_name="emails")
    version = models.CharField(max_length=50, default='1')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s,%s' % (self.login, self.password)
