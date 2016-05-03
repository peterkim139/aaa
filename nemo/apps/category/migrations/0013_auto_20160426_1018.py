# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0012_auto_20160119_0718'),
    ]

    operations = [
        migrations.AddField(
            model_name='params',
            name='address',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='params',
            name='city',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='params',
            name='latitude',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='params',
            name='longitude',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='params',
            name='postal_code',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='params',
            name='state',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
