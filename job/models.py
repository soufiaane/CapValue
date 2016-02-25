from django.db import models

from authentication.models import Account
from seed.models import Seed


class Job(models.Model):
    STATUS_OPTIONS = (
        ('PND', 'Pending'),
        ('RUN', 'Running'),
        ('PSD', 'Paused'),
        ('END', 'Finished')
    )
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="jobs", null=True)
    seeds = models.ForeignKey(Seed, related_name='jobs', null=True)
    subject = models.CharField(max_length=200, default='')
    actions = models.CharField(max_length=200, default='RS')
    status = models.CharField(max_length=3, choices=STATUS_OPTIONS, default='PND')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}'.format(self.subject)
