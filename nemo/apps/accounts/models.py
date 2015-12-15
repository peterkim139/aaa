from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxLengthValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from decimal import Decimal
from accounts.managers import AuthUserManager, AbstractDateTime



class User(AbstractDateTime, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True,blank=False,default='')
    first_name = models.CharField(max_length=255, blank=False,default='')
    last_name = models.CharField(max_length=255, blank=False,default='')
    merchant_id = models.CharField(max_length=255, blank=True,default='')
    customer_id = models.CharField(max_length=255, blank=True,default='')
    phone_number = models.CharField(max_length=255,blank=False,default='')
    STATUS_TYPES = (('admin', 'admin'),('client', 'client'))
    role = models.CharField(max_length=5,choices=STATUS_TYPES,default='client')
    is_staff = models.BooleanField(default=0)
    is_active = models.BooleanField(default=1)
    objects = AuthUserManager()
    USERNAME_FIELD = 'email'


    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return unicode(self.email) or 'not found'

    class Meta:
        ordering = ["id"]
        db_table = "user"
        get_latest_by = "created"