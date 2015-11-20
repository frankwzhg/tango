# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideosModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_name', models.CharField(unique=True, max_length=128)),
                ('video_path', models.ImageField(upload_to=b'learn')),
                ('upload_date', models.DateField(default=django.utils.timezone.now)),
                ('video_owner', models.CharField(max_length=50, blank=True)),
            ],
        ),
    ]
