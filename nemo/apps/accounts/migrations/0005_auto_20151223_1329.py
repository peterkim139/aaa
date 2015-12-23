# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20151223_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='reset_key',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
