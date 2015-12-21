# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rent_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
