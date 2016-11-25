from __future__ import unicode_literals

from django.db import models

class Diagram(models.Model):
    name = models.CharField(max_length=254, unique=True)
    diagram = models.TextField()
