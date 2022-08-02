from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from wheezy.validation import Validator
from wheezy.validation.rules import required, length
from gatewaynum import message

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=50, unique=True, db_index=True)
    email = models.EmailField(_('email address'), max_length=255, blank=True, null=True, unique=True, db_index=True)
    is_active = models.BooleanField(_('active'), default=True)
    iaccesslevel = models.SmallIntegerField(_('iaccesslevel'))
    ip = models.CharField(_('ip'), max_length=20, blank=True)
    itopupaccesslevel = models.SmallIntegerField(_('itopupaccesslevel'), null=True)
    twholesaler = models.CharField(_('twholesaler'), max_length=50)
    featureflag = models.CharField(_('featureflag'), max_length=20, blank=True, null=True)
    functionflag = models.CharField(_('functionflag'), max_length=20, blank=True, null=True)
    department = models.CharField(_('department'), max_length=50, blank=True, null=True)
    admin = models.SmallIntegerField(_('admin'), null=True)
    expiry = models.DateTimeField(_('expiry'), null=True)
    
    USERNAME_FIELD = 'username'
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
 
    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
        
    def __unicode__(self):
        return self.username
    
class Account(object):
    
    def __init__(self):
        self.username = None
        self.password = None
        
    def validate(self):
        v = Validator({
            'username': [required(message_template=message.required_msg('User ID'))],
            'password': [required(message_template=message.required_msg('User Password'))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
    
class AccountRenew(object):
    
    def __init__(self):
        self.username = None
        self.password = None
        self.newpassword = None
        self.confirmpassword = None
        
    def validate(self):
        v = Validator({
            'password': [required(message_template=message.required_msg('Existing Password'))],
            'newpassword': [required(message_template=message.required_msg('New Password')),
                            length(min=6, message_template=message.minlen_msg('New Password', 6))],
            'confirmpassword': [required(message_template=message.required_msg('Confirm Password'))]
        })
        errors = {}
        b = v.validate(self, results=errors)
        l = message.get_error_list(errors)
        
        return l
    