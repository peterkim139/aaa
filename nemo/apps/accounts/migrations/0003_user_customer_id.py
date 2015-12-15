# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_merchant_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='customer_id',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
