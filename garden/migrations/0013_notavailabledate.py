# Generated by Django 5.0.4 on 2024-10-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garden', '0012_service_availability'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotAvailableDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
