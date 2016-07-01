# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0019_rent_start_date'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='rent',
            table='rrent',
        ),
    ]
