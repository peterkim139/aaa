# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_auto_20160919_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='param_image',
            field=models.OneToOneField(null=True, to='category.Params'),
        ),
    ]
