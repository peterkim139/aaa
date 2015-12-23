# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0014_auto_20151222_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='price',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='rent',
            name='transaction_status',
            field=models.CharField(default=b'pending', max_length=30, choices=[(b'pending', b'pending'), (b'error', b''), (b'settled', b'settled')]),
        ),
    ]
