# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_stream', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='name',
            field=models.CharField(default=b'song', unique=True, max_length=128),
            preserve_default=True,
        ),
    ]
