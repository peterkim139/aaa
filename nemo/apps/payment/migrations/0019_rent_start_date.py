# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0018_auto_20160204_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
