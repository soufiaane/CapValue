from django.db import models
from authentication.models import Account
from boites.models import Boites


class Seed(models.Model):
    user = models.ForeignKey(Account)
    seed_label = models.CharField(max_length=40, blank=True)
    boites = models.ForeignKey(Boites)
