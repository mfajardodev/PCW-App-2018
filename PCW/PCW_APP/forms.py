# -*- coding: utf-8 -*-
# @Author: Chris Kim
# @Date:   2018-02-24 16:17:33
# @Last Modified by:   Chris Kim
# @Last Modified time: 2018-03-16 17:32:06

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _

class SignUpForm(UserCreationForm):

   email = forms.EmailField(max_length=254, help_text=
      'Use your Cal Poly Email. Email must not already be in use. If these requirements are not met you will be redirect to this page.' )


   class Meta:
      model = User
      model.username.widget = forms.TextInput(attrs={'class': 'form-control'})
      fields = ('username', 'email', 'password1', 'password2', )