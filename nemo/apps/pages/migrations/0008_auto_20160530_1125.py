# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_auto_20160530_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='user1_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='thread',
            name='user2_id',
            field=models.IntegerField(),
        ),
    ]
