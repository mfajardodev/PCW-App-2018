# -*- coding: utf-8 -*-
# @Author: Chris Kim
# @Date:   2018-01-25 19:51:43
# @Last Modified by:   Chris Kim
# @Last Modified time: 2018-03-16 17:56:13
from django.conf.urls import url
from django.urls import re_path
from django.urls import path, include
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [

    re_path(r'^signup/$', views.signup, name='signup'),
   	re_path(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    re_path(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    re_path(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    path('', auth_views.login, {'template_name': 'account/login.html'}, name='login'),
    path('home', views.home, name='home'),
    path('data', views.data, name='data'),
    path('maps', views.maps, name='maps'),
    path('pamphlet', views.pamphlet, name='pamphlet'),
    path('schedule', views.schedule, name='schedule'),
    path('account/profile', views.profile, name='profile'),
    path('account/account_activation_sent', views.account_activation_sent, name='account_activation_sent'),

]