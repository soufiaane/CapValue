from django.db import models
from authentication.models import Account
from mail.models import Email


class FSResults(models.Model):
    owner = models.ManyToManyField(Account, related_name='fsResults')
    from_email = models.CharField(max_length=255, blank=True)
    sender_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, blank=True, null=True)
    received_date = models.DateTimeField()
    found_in = models.ManyToManyField(Email, related_name='fsResults')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s,%s' % (self.from_email, self.sender_ip)
