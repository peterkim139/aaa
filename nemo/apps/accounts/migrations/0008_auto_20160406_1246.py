# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='zip_code',
            field=models.CharField(default=b'', max_length=10),
        ),
    ]
