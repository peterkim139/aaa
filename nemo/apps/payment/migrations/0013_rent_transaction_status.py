# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_auto_20151222_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='transaction_status',
            field=models.CharField(default=b'pending', max_length=30, choices=[(b'pending', b'pending'), (b'error', b'error'), (b'settled', b'settled')]),
        ),
    ]
