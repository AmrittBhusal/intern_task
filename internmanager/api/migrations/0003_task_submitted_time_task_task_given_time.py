# Generated by Django 5.0.6 on 2024-06-06 11:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='submitted_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='task',
            name='task_given_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
