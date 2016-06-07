# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_billing_customer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='customer_number',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='billing',
            name='customer_id',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='billing',
            name='is_default',
            field=models.BooleanField(),
        ),
    ]
