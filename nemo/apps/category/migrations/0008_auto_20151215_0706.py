# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0007_auto_20151215_0706'),
    ]

    operations = [
        migrations.RenameField(
            model_name='params',
            old_name='item_owner_id',
            new_name='item_owner',
        ),
    ]
