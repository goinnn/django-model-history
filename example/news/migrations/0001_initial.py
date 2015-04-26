# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BaseNewsHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('history_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('history_status', models.CharField(default=b'update', max_length=6, verbose_name='Status', choices=[(b'insert', 'Insert'), (b'update', 'Update'), (b'delete', 'Delete')])),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'base news change history',
                'verbose_name_plural': 'base news change histories',
            },
        ),
        migrations.CreateModel(
            name='EventHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('history_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('history_status', models.CharField(default=b'update', max_length=6, verbose_name='Status', choices=[(b'insert', 'Insert'), (b'update', 'Update'), (b'delete', 'Delete')])),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('start_date', models.DateTimeField(verbose_name='Start date')),
                ('end_date', models.DateTimeField(verbose_name='End date')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Event change history',
                'verbose_name_plural': 'Event change histories',
            },
        ),
        migrations.CreateModel(
            name='NewsItemHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('history_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('history_status', models.CharField(default=b'update', max_length=6, verbose_name='Status', choices=[(b'insert', 'Insert'), (b'update', 'Update'), (b'delete', 'Delete')])),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('publish_date', models.DateTimeField(verbose_name='Publish date')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'News item change history',
                'verbose_name_plural': 'News item change histories',
            },
        ),
        migrations.CreateModel(
            name='NewsItemV2History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('history_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('history_status', models.CharField(default=b'update', max_length=6, verbose_name='Status', choices=[(b'insert', 'Insert'), (b'update', 'Update'), (b'delete', 'Delete')])),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('publish_date', models.DateTimeField(verbose_name='Publish date')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'News item (Version 2) change history',
                'verbose_name_plural': 'News item (Version 2) change histories',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('basenews_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='news.BaseNews')),
                ('start_date', models.DateTimeField(verbose_name='Start date')),
                ('end_date', models.DateTimeField(verbose_name='End date')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
            bases=('news.basenews',),
        ),
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('basenews_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='news.BaseNews')),
                ('publish_date', models.DateTimeField(verbose_name='Publish date')),
            ],
            options={
                'verbose_name': 'News item',
                'verbose_name_plural': 'News',
            },
            bases=('news.basenews',),
        ),
        migrations.CreateModel(
            name='NewsItemV2',
            fields=[
                ('basenews_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='news.BaseNews')),
                ('publish_date', models.DateTimeField(verbose_name='Publish date')),
            ],
            options={
                'verbose_name': 'News item (Version 2)',
                'verbose_name_plural': 'News (Version 2)',
            },
            bases=('news.basenews',),
        ),
        migrations.AddField(
            model_name='basenewshistory',
            name='history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='news.BaseNews', null=True),
        ),
        migrations.AddField(
            model_name='newsitemv2history',
            name='history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='news.NewsItemV2', null=True),
        ),
        migrations.AddField(
            model_name='newsitemhistory',
            name='history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='news.NewsItem', null=True),
        ),
        migrations.AddField(
            model_name='eventhistory',
            name='history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='news.Event', null=True),
        ),
    ]
