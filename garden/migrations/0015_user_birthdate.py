# Generated by Django 5.0.4 on 2024-10-10 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0014_delete_notavailabledate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]