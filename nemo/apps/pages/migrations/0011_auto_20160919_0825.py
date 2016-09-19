# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_thread_item_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='item_id',
            field=models.ForeignKey(to='category.Params'),
        ),
    ]
