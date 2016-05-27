# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20160527_0630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='thread_id',
            new_name='thread',
        ),
    ]
