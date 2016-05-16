# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20160406_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.FileField(null=True, upload_to=b'images', blank=True),
        ),
    ]
