# -*- coding: utf-8 -*-
# @Author: Chris Kim
# @Date:   2018-02-24 16:17:33
# @Last Modified by:   Chris Kim
# @Last Modified time: 2018-03-02 18:17:02

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


    class Meta:
        model = User
        model.username.widget = forms.TextInput(attrs={'class': 'form-control'})
        fields = ('username', 'email', 'birth_date', 'password1', 'password2', )