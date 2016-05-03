from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from decimal import Decimal
from accounts.managers import  AbstractDateTime
from accounts.models import User
from category.models import Params

class Image(models.Model):

    param_image = models.ForeignKey(Params)
    #name = models.FileField(upload_to = 'images/items/', null=True,blank=False)
    name = models.CharField(max_length=255, blank=False, default='')
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    modified = models.DateTimeField(auto_now=True,auto_now_add=False)

    class Meta:
        ordering = ["id"]
        db_table = "images"
        get_latest_by = "created"