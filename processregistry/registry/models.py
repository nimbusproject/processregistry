from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ProcessDefinition(models.Model):
    user = models.ForeignKey(User, editable=False)
    definition = models.CharField(max_length=1024)
