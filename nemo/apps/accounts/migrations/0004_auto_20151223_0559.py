# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_key',
            field=models.CharField(default=None, max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(default=b'client', max_length=10,
                                   choices=[(b'admin', b'admin'), (b'client', b'client')]),
        ),
    ]
