# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0008_auto_20151215_0706'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(default=b'pending', max_length=30, choices=[(b'pending', b'pending'), (b'approved', b'approved'), (b'canceled', b'canceled')])),
                ('price', models.DecimalField(default=0, max_digits=5, decimal_places=2)),
                ('rent_date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('param', models.ForeignKey(to='category.Params')),
                ('user', models.ForeignKey(related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'db_table': 'rent',
                'get_latest_by': 'created',
            },
        ),
    ]
