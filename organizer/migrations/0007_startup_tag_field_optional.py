# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-05 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizer', '0006_newslink_unique_together_slug_startup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='tags',
            field=models.ManyToManyField(blank=True, to='organizer.Tag'),
        ),
    ]
