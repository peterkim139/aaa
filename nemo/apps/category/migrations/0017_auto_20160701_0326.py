# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0016_params_street'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='params',
            table='items',
        ),
    ]
