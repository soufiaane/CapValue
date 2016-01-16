from datetime import datetime

from django.db import models
from authentication.models import Account
from seed.models import Seed


class Job(models.Model):
    STATUS_OPTIONS = (
        ('PND', 'Pending'),
        ('RN', 'Running'),
        ('Ps', 'Paused'),
        ('END', 'Finished')
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    seed_list = models.ManyToManyField(Seed, related_name='jobs')
    keywords = models.CharField(max_length=10, default='')
    actions = models.CharField(max_length=30, default='RS')
    status = models.CharField(max_length=3, choices=STATUS_OPTIONS, default='PND')

    created_at = models.DateTimeField(auto_now_add=True, default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True, default=datetime.now)

