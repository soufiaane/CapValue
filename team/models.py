from django.db import models

from authentication.models import Account
from isp.models import ISP


class Team(models.Model):
    name = models.CharField(max_length=40, blank=True)
    members = models.ManyToManyField(Account, related_name='teams')
    logo = models.CharField(max_length=40, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.name
