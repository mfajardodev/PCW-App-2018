# -*- coding: utf-8 -*-
# @Author: Chris Kim
# @Date:   2018-03-02 18:14:38
# @Last Modified by:   Chris Kim
# @Last Modified time: 2018-03-02 18:14:43

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()