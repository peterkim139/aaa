# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_status',
            field=models.CharField(default=1, max_length=1),
        ),
    ]
