# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20151218_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='price',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=1),
        ),
    ]
