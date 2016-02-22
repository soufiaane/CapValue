from authentication.models import Account
from django.db import models


class ISP(models.Model):
    isp_name = models.CharField(max_length=40, blank=True)
    members = models.ForeignKey(Account, related_name='isp', null=True)
    logo = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % isp_name
