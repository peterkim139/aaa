# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20160601_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.FileField(default=None, null=True, upload_to=b'images/users', blank=True),
        ),
    ]
