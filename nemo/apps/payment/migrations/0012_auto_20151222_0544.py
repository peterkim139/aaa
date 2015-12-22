# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_rent_transaction_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rent',
            name='transaction_status',
        ),
        migrations.AlterField(
            model_name='rent',
            name='status',
            field=models.CharField(default=b'pending', max_length=30, choices=[(b'seller_declined', b'seller_declined'), (b'customer_declined', b'customer_declined'), (b'pending', b'pending'), (b'approved', b'approved'), (b'paid', b'paid'), (b'customer_canceled', b'customer_canceled'), (b'seller_canceled', b'seller_canceled')]),
        ),
    ]
