# Generated by Django 5.0.4 on 2024-10-12 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0016_user_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_picture',
        ),
    ]