# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0016_auto_20151225_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='status',
            field=models.CharField(default=b'pending', max_length=30, choices=[(b'seller_declined', b'seller_declined'), (b'customer_declined', b'customer_declined'), (b'pending', b'pending'), (b'approved', b'approved'), (b'expired', b'expired'), (b'paid', b'paid'), (b'customer_canceled', b'customer_canceled'), (b'seller_canceled', b'seller_canceled')]),
        ),
        migrations.AlterField(
            model_name='rent',
            name='transaction_status',
            field=models.CharField(default=b'pending', max_length=30, choices=[(b'pending', b'pending'), (b'error', b''), (b'merchant', b'merchant'), (b'settled', b'settled')]),
        ),
    ]
