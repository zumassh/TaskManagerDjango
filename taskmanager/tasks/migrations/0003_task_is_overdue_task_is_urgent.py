# Generated by Django 5.2 on 2025-05-08 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_remove_task_is_urgent'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_overdue',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='is_urgent',
            field=models.BooleanField(default=False),
        ),
    ]
