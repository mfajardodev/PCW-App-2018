import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

# class User(models.Model):
#    email = models.CharField(max_length=200)
#    registered = models.IntegerField(default=0)
#    username = models.CharField(max_length=200)
#    password = models.CharField(max_length=200)

class Events(models.Model):
    title = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=15,  null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=6, default=0, null=True)
    lng = models.DecimalField(max_digits=10, decimal_places=6, default=0, null=True)
    day = models.CharField(max_length=10,  null=True)
    startTime = models.DateTimeField(null=True, blank=True)
    endTime = models.DateTimeField(null=True, blank=True)

class Days(models.Model):
     name = models.CharField(max_length=10)

class SignInTime(models.Model):
    startTime = models.DateTimeField(null=True, blank=True)
    endTime = models.DateTimeField(null=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    QR_code = models.URLField(null=True)
    signed_in = models.BooleanField(default=False)
    Organization = models.CharField(max_length=30, blank=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    print(instance)
    if not Profile.objects.all().filter(user=instance).exists():
        Profile.objects.create(user=instance)
    instance.profile.save()
