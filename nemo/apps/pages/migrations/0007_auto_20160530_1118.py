# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20160527_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='from_user_id',
            field=models.ForeignKey(related_name='from_user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='to_user_id',
            field=models.ForeignKey(related_name='to_user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='thread',
            name='user1_id',
            field=models.ForeignKey(related_name='user1_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='thread',
            name='user2_id',
            field=models.ForeignKey(related_name='user2_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
