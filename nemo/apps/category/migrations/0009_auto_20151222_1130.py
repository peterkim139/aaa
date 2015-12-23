# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0008_auto_20151215_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='params',
            name='price',
            field=models.FloatField(default=0, null=True, blank=True),
        ),
    ]
