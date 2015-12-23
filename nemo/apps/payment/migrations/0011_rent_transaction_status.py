# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_auto_20151218_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='transaction_status',
            field=models.CharField(default=b'pending', max_length=30, choices=[(b'pending', b'pending'), (b'settled', b'settled')]),
        ),
    ]
