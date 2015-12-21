# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20151218_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='status',
            field=models.CharField(default=b'pending', max_length=30, choices=[(b'seller_declined', b'seller_declined'), (b'customer_declined', b'customer_declined'), (b'pending', b'pending'), (b'approved', b'approved'), (b'customer_canceled', b'customer_canceled'), (b'seller_canceled', b'seller_canceled')]),
        ),
    ]
