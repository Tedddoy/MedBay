# Generated by Django 5.1.1 on 2024-10-05 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0003_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]
