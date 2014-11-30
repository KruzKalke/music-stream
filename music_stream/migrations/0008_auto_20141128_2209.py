# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_stream', '0007_song_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='album_slug',
            field=models.SlugField(default=b'unknown', max_length=128),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='artist_slug',
            field=models.SlugField(default=b'unknown', max_length=128),
            preserve_default=True,
        ),
    ]
