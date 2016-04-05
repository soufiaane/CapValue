from django.db import models
from domain.models import Domain


class SPF(models.Model):
    domain = models.ManyToManyField(Domain, related_name="spf")
    result = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s,%s' % self.result
