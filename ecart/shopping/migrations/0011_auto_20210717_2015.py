# Generated by Django 3.1.5 on 2021-07-17 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0010_logs_profile_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='award1',
            new_name='project',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='award2',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='award3',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='award4',
        ),
    ]
