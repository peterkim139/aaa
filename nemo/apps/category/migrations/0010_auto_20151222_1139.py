# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0009_auto_20151222_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='params',
            name='price',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
        ),
    ]
