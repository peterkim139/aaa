# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0014_auto_20160519_0633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='params',
            name='delete',
        ),
        migrations.RemoveField(
            model_name='params',
            name='publish',
        ),
        migrations.AddField(
            model_name='params',
            name='status',
            field=models.CharField(default=b'published', max_length=11, choices=[(b'published', b'published'), (b'unpublished', b'unpublished'), (b'deleted', b'deleted')]),
        ),
    ]
