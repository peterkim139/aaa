# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20151215_0703'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='rent_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
