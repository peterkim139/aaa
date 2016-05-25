# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0013_auto_20160426_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='params',
            name='delete',
            field=models.CharField(default=b'not_deleted', max_length=30, choices=[(b'deleted', b'deleted'), (b'not_deleted', b'not_deleted')]),
        ),
        migrations.AddField(
            model_name='params',
            name='publish',
            field=models.CharField(default=b'published', max_length=30, choices=[(b'published', b'published'), (b'unpublished', b'unpublished')]),
        ),
    ]
