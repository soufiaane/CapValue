from django.db import models
from authentication.models import Account
import uuid


class Seed(models.Model):
    user = models.ForeignKey(Account)
    actions = models.DateTimeField(auto_now=True)

    jobid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid1())
    entered = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(blank=True)

    keyword = models.CharField(max_length=40, blank=True)
    status = models.BooleanField(default=False)
    processed = models.IntegerField(default=0)
