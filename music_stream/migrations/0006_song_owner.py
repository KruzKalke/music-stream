# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music_stream', '0005_auto_20141128_0505'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='owner',
            field=models.CharField(default=None, max_length=30),
            preserve_default=True,
        ),
    ]
