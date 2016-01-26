from authentication.models import Account
from emails.models import Email
from django.db import models


class Seed(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    emails = models.ManyToManyField(Email, related_name='seed')
    list_name = models.CharField(max_length=40, blank=True)
    proxyType = models.CharField(max_length=40, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0}'.format(self.list_name)
