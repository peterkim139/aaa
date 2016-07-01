# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0017_auto_20160701_0326'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='porperty_values',
            table='property_values',
        ),
    ]
