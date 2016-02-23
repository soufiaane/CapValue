from django.db import models

from authentication.models import Account
from isp.models import ISP


class Team(models.Model):
    team_name = models.CharField(max_length=40, blank=True)
    team_leader = models.ForeignKey(Account, on_delete=models.CASCADE)
    team_members = models.ForeignKey(Account, related_name='teams', null=True)
    isp = models.ManyToManyField(ISP, related_name='teams')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % team_name
