from authentication.models import Account
from django.db import models


class ISP(models.Model):
    isp_name = models.CharField(max_length=40, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0}'.format(self.team_name)
