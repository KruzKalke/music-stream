# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_stream', '0003_auto_20141118_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(unique=True, max_length=128)),
                ('songfile', models.FileField(upload_to=b'music/%Y/%m/%d')),
                ('title', models.CharField(default=b'untitled', max_length=128)),
                ('artist', models.CharField(default=b'unknown', max_length=128)),
                ('track_num', models.PositiveSmallIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
