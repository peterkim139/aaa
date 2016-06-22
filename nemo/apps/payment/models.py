from django.db import models
from django.utils import timezone
from accounts.mixins import AbstractDateTime
from category.models import Params
from accounts.models import User


class Rent(AbstractDateTime):

    param = models.ForeignKey(Params)
    user = models.ForeignKey(User,related_name='order')
    owner = models.ForeignKey(User,related_name='item_owner')
    STATUS_TYPES = (('seller_declined', 'seller_declined'),
                    ('customer_declined', 'customer_declined'),
                    ('pending', 'pending'),
                    ('approved', 'approved'),
                    ('expired','expired'),
                    ('paid', 'paid'),
                    ('customer_canceled', 'customer_canceled'),
                    ('admin_canceled', 'admin_canceled'),
                    ('seller_canceled', 'seller_canceled'))
    TRANSACTION_STATUS = (('pending','pending'),
                          ('error',''),
                          ('merchant','merchant'),
                          ('settled','settled'))
    status = models.CharField(max_length=30, choices=STATUS_TYPES,default='pending')
    transaction = models.CharField(max_length=255, blank=True,default='')
    transaction_status = models.CharField(max_length=30, choices=TRANSACTION_STATUS,default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    start_date = models.DateTimeField(default=timezone.now)
    rent_date = models.DateTimeField(default=timezone.now)
    def __unicode__(self):
        return unicode(self.status) or 'not found'

    class Meta:
        ordering = ["id"]
        db_table = "rent"
        get_latest_by = "created"


