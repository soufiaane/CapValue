from authentication.models import Account
from isp.models import ISP
from django.db import models


class Team(models.Model):
    team_name = models.CharField(max_length=40, blank=True)
    team_leader = models.ForeignKey(Account, on_delete=models.CASCADE)
    team_members = models.ManyToManyField(Account, related_name='teams')
    isp = models.ManyToManyField(ISP, related_name='teams')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0}'.format(self.team_name)
