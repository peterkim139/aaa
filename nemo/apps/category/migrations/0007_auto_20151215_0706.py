# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_params_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='params',
            old_name='user',
            new_name='item_owner_id',
        ),
    ]
