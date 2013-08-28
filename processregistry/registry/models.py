from django.db import models

# Create your models here.


class ProcessDefinition(models.Model):
    definition = models.CharField(max_length=1024)
