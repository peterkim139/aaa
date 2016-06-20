from django.db import models
from django.core.validators import MaxLengthValidator
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

class Properties(AbstractDateTime,models.Model):

    sub_category = models.ForeignKey(SubCategory,related_name='title')
    property_name  = models.CharField(max_length=255, unique=True)
    PROPERTY_TYPES = (('checkbox', 'checkbox'),('select', 'select'),('input', 'input'))
    property_type = models.CharField(max_length=10,choices=PROPERTY_TYPES,default='select')

    def __unicode__(self):
        return unicode(self.property_name) or 'not found'

    class Meta:
        ordering = ["id"]
        db_table = "properties"
        get_latest_by = "created"

class Porperty_values(AbstractDateTime,models.Model):

    property = models.ForeignKey(Properties,related_name='property')
    value_name  = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return unicode(self.value_name) or 'not found'

    class Meta:
        ordering = ["id"]
        db_table = "porperty_values"
        get_latest_by = "created"
        # verbose_name_plural = 'Values'


class Params(AbstractDateTime,models.Model):

    subcategory = models.ForeignKey(SubCategory)
    item_owner = models.ForeignKey(User)
    name = models.CharField(max_length=255, blank=False,default='')
    price = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    description  = models.TextField(blank=False,null=False,validators=[MaxLengthValidator(200)],default='')
    address = models.CharField(max_length=255, blank=False, default='')
    state = models.CharField(max_length=255, blank=False, default='')
    city = models.CharField(max_length=255, blank=False, default='')
    postal_code = models.CharField(max_length=255, blank=False, default='')
    latitude = models.CharField(max_length=255, blank=False, default='')
    longitude = models.CharField(max_length=255, blank=False, default='')
    PUBLISH_TYPES = (('published', 'published'),
                    ('unpublished', 'unpublished'),
                    ('deleted','deleted'))
    status = models.CharField(max_length=11, choices=PUBLISH_TYPES, default='published')


    def __unicode__(self):
        return unicode(self.name) or 'not found'

    class Meta:
        ordering = ["id"]
        db_table = "parametrs"
        get_latest_by = "created"

