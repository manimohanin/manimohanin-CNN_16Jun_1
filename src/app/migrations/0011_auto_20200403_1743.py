# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-03 12:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200403_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/clean'),
        ),
    ]
