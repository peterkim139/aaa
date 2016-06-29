# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0015_auto_20160523_0745'),
    ]

    operations = [
        migrations.AddField(
            model_name='params',
            name='street',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
