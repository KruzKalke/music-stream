# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_stream', '0002_music_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='name',
            field=models.CharField(unique=True, max_length=128),
        ),
    ]
