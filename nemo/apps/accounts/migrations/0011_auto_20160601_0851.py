# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20160513_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.FileField(null=True, upload_to=b'images/users'),
        ),
    ]
