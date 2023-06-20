# Generated by Django 4.2 on 2023-05-20 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_alter_profile_time_joined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='time_joined',
        ),
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='My Bio says...', max_length=150),
        ),
    ]