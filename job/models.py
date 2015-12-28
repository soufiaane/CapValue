from django.db import models
from authentication.models import Account
from seed.models import Seed
import uuid


class Job(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    # seed_list = models.ForeignKey(Seed)
    actions = models.ManyToManyRel

    entered = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(blank=True)

    keyword = models.CharField(max_length=40, blank=True)
    status = models.BooleanField(default=False)
    processed = models.IntegerField(default=0)
