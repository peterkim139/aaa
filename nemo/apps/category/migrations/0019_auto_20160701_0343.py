# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0018_auto_20160701_0329'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='params',
            table='parametrs',
        ),
        migrations.AlterModelTable(
            name='porperty_values',
            table='porperty_values',
        ),
    ]
