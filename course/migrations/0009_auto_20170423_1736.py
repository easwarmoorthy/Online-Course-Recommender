# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-23 17:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_coursereviewmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursereviewmodel',
            name='course',
        ),
        migrations.AddField(
            model_name='coursereviewmodel',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.CourseModel'),
        ),
    ]
