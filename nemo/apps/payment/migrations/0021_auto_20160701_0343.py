# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0020_auto_20160701_0341'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='rent',
            table='rent',
        ),
    ]
