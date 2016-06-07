# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_billing'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='customer_name',
            field=models.CharField(default=b'', max_length=255, blank=True),
        ),
    ]
