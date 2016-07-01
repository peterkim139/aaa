# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0019_auto_20160701_0343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['id'], 'get_latest_by': 'created', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='params',
            options={'ordering': ['id'], 'get_latest_by': 'created', 'verbose_name_plural': 'Items'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ['id'], 'get_latest_by': 'created', 'verbose_name_plural': 'Subcategories'},
        ),
    ]
