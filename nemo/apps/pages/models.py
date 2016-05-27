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
    image_name = models.CharField(max_length=255, blank=False, default='')
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    modified = models.DateTimeField(auto_now=True,auto_now_add=False)

    class Meta:
        ordering = ["id"]
        db_table = "images"
        get_latest_by = "created"

class Thread(models.Model):
    last_message = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    modified = models.DateTimeField(auto_now=True,auto_now_add=False)
    user1_id = models.IntegerField()
    user2_id = models.IntegerField()

    class Meta:
        db_table = 'thread'

class Message(models.Model):
    thread = models.ForeignKey(Thread)
    unread = models.IntegerField()
    message = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now=False,auto_now_add=True)
    modified = models.DateTimeField(auto_now=True,auto_now_add=False)
    from_user_id = models.IntegerField()
    to_user_id = models.IntegerField()

    class Meta:
        db_table = 'message'