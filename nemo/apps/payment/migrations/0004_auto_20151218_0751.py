# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20151218_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='price',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
        ),
    ]
