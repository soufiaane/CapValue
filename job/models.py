from django.db import models

from authentication.models import Account
from seed.models import Seed


class Job(models.Model):
    Action_CHOICES = (
        ('RS', 'Mark spam as read'),
        ('NS', 'Not spam'),
        ('RI', 'Mark inbox as read'),
        ('OI', 'Open inbox'),
        ('TR', 'Trust inbox mail'),
        ('SS', 'Safe spam mail'),
        ('AC', 'Add contacts INBOX'),
        ('CL', 'Click links INBOX'),
        ('FM', 'Flag Mails INBOX')
    )
    STATUS_OPTIONS = (
        ('RS', 'Mark spam as read'),
        ('CL', 'Click links INBOX'),
        ('FM', 'Flag Mails INBOX')
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    seed_list = models.ManyToManyField(Seed)
    actions = models.CharField(max_length=2, choices=Action_CHOICES, default='RS')
    status = models.CharField(max_length=2, choices=STATUS_OPTIONS, default='CL')

    entered = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(blank=True, auto_now_add=True)

    keyword = models.CharField(max_length=40, blank=True)
    processed = models.IntegerField(default=0)
