# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_auto_20151218_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='status',
            field=models.CharField(default=b'pending', max_length=30, choices=[(b'decline', b'decline'), (b'pending', b'pending'), (b'approved', b'approved'), (b'canceled', b'canceled')]),
        ),
    ]
