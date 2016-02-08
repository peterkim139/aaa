# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20151223_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='credits',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
        ),
    ]
