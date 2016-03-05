from django.db import models

from authentication.models import Account
from mail.models import Email


class Seed(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='seeds', null=True)
    emails = models.ForeignKey(Email, related_name='seed', null=True)
    name = models.CharField(max_length=40, blank=True)
    proxy = models.CharField(max_length=40, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % list_name
