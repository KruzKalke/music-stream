# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import music_stream.models


class Migration(migrations.Migration):

    dependencies = [
        ('music_stream', '0008_auto_20141128_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('musicfile', models.FileField(upload_to=b'music/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='song',
            name='md5sum',
            field=models.CharField(default=None, max_length=36),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='song',
            name='file_name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='song',
            name='songfile',
            field=models.FileField(storage=music_stream.models.CustomStorage(), upload_to=b'music/%Y/%m/%d'),
        ),
    ]
