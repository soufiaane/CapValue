from datetime import datetime
from django.db import models
from authentication.models import Account


class Seed(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    list_name = models.CharField(max_length=40, blank=True)
    proxyType = models.CharField(max_length=40, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True, default=datetime.now)

    def __unicode__(self):
        return '{0}'.format(self.list_name)