# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-23 16:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20170423_1614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursereviewmodel',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursereviewmodel',
            name='user',
        ),
        migrations.DeleteModel(
            name='CoursereviewModel',
        ),
    ]
