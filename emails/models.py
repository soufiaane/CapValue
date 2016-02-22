from authentication.models import Account
from django.db import models


class Email(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="emails")
    login = models.CharField(max_length=40, blank=True)
    password = models.CharField(max_length=40, blank=True)
    isActive = models.BooleanField(default=True)
    version = models.CharField(max_length=2, blank=True, default='V1')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s,%s' % (self.login, self.password)
