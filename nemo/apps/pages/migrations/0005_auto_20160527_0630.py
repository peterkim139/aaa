# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20160505_0644'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unread', models.IntegerField()),
                ('message', models.TextField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('from_user_id', models.IntegerField()),
                ('to_user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_message', models.TextField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user1_id', models.IntegerField()),
                ('user2_id', models.IntegerField()),
            ],
            options={
                'db_table': 'thread',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='thread_id',
            field=models.ForeignKey(to='pages.Thread'),
        ),
    ]
