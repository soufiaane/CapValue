from django.db import models


class Boites(models.Model):
    boite_label = models.CharField(max_length=40, blank=True)
    # boites = models.ForeignKey()
