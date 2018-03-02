# -*- coding: utf-8 -*-
# @Author: Chris Kim
# @Date:   2018-01-25 19:51:43
# @Last Modified by:   Chris Kim
# @Last Modified time: 2018-03-01 00:47:54

from django.urls import re_path
from django.urls import path, include
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [

    re_path(r'^signup/$', views.signup, name='signup'),
    path('', auth_views.login, {'template_name': 'account/login.html'}, name='login'),
   	re_path(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('home', views.home, name='home')

]