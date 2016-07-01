# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20160701_0405'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'get_latest_by': 'created'},
        ),
        migrations.AddField(
            model_name='user',
            name='profile_status',
            field=models.BooleanField(default=1),
        ),
    ]
