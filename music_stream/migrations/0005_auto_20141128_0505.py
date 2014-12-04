# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_stream', '0004_song'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Music',
        ),
        migrations.AddField(
            model_name='song',
            name='length',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
