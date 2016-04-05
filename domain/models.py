from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s,%s' % (self.login, self.password)
