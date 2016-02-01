# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0010_auto_20151222_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('property_name', models.CharField(unique=True, max_length=255)),
                ('property_type', models.CharField(default=b'select', max_length=10, choices=[(b'checkbox', b'checkbox'), (b'select', b'select')])),
                ('sub_category', models.ForeignKey(related_name='title', to='category.SubCategory')),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'properties',
                'get_latest_by': 'created',
            },
        ),
    ]
