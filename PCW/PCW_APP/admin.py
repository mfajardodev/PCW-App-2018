from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Events)
admin.site.register(Days)
admin.site.register(SignInTime)
admin.site.register(Profile)