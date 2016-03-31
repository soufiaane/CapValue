from django.db import models

from authentication.models import Account


class ISP(models.Model):
    teams = models.ManyToManyField(Account, related_name="isp", blank=True)
    name = models.CharField(max_length=40)
    logo = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.name
