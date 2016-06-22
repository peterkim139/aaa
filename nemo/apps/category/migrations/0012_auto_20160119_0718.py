# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0011_properties'),
    ]

    operations = [
        migrations.CreateModel(
            name='Porperty_values',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('value_name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'porperty_values',
                'get_latest_by': 'created',
            },
        ),
        migrations.AlterField(
            model_name='properties',
            name='property_type',
            field=models.CharField(default=b'select', max_length=10,
                                   choices=[(b'checkbox', b'checkbox'), (b'select', b'select'), (b'input', b'input')]),
        ),
        migrations.AddField(
            model_name='porperty_values',
            name='property',
            field=models.ForeignKey(related_name='property', to='category.Properties'),
        ),
    ]
