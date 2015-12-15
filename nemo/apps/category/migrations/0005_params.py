# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_auto_20151210_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Params',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('price', models.DecimalField(default=0, max_digits=5, decimal_places=2)),
                ('name', models.CharField(default=b'', max_length=255)),
                ('description', models.TextField(default=b'', validators=[django.core.validators.MaxLengthValidator(200)])),
                ('subcategory', models.ForeignKey(to='category.SubCategory')),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'parametrs',
                'get_latest_by': 'created',
            },
        ),
    ]
