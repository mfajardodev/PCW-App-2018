import datetime
from django.db import models
from django.utils import timezone
# Create your models here.

class User(models.Model):
   email = models.CharField(max_length=200)
   registered = models.IntegerField(default=0)
   username = models.CharField(max_length=200)
   password = models.CharField(max_length=200)