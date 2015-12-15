from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from decimal import Decimal
from accounts.managers import  AbstractDateTime
from accounts.models import User

class Category(AbstractDateTime,models.Model):
    name = models.CharField(max_length=255, blank=False,default='')
    def __unicode__(self):
        return unicode(self.name) or 'not found'

    class Meta:
        ordering = ["id"]
        db_table = "category"
        get_latest_by = "created"


class SubCategory(AbstractDateTime,models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=255, blank=False,default='')
    def __unicode__(self):
        return unicode(self.name) or 'not found'

    class Meta:
        ordering = ["id"]
        db_table = "sub_category"
        get_latest_by = "created"


class Params(AbstractDateTime,models.Model):

    subcategory = models.ForeignKey(SubCategory)
    item_owner = models.ForeignKey(User)
    name = models.CharField(max_length=255, blank=False,default='')
    price = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    description  = models.TextField(blank=False,null=False,validators=[MaxLengthValidator(200)],default='')
    def __unicode__(self):
        return unicode(self.name) or 'not found'

    class Meta:
        ordering = ["id"]
        db_table = "parametrs"
        get_latest_by = "created"