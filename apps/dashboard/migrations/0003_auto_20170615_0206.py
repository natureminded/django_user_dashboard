# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-15 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20170615_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='sender',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments_sent', to='dashboard.User'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_sent', to='dashboard.User'),
        ),
    ]