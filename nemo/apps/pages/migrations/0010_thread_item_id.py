# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_auto_20160629_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='item_id',
            field=models.IntegerField(default=1),
        ),
    ]
