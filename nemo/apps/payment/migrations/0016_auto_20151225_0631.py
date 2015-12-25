# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0015_auto_20151222_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='owner',
            field=models.ForeignKey(related_name='item_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
