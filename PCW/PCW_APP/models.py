import datetime
from django.db import models
from django.utils import timezone
# Create your models here.

class User(models.Model):
   email = models.CharField(max_length=200)
   registered = models.IntegerField(default=0)
   username = models.CharField(max_length=200)
   password = models.CharField(max_length=200)

class Markers(models.Model):
   name = models.CharField(max_length=60)
   address = models.CharField(max_length=80)
   lat = models.FloatField(max_digits=10, decimal_places=6)
   lng = models.FloatField(max_digits=10, decimal_places=6)
   type = models.CharField(max_length=30)

class Events(models.Model):
   title = models.CharField(max_length=50)
   location = models.CharField(max_length=60)
   day = models.CharField(max_length=10)
   startTime = models.DateTimeField()
   endTime = models.DateTimeField()

class Days(models.Model);
   name = models.CharField(max_length=10)
