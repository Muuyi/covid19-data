# Generated by Django 3.1 on 2020-08-22 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20200822_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coviddata',
            name='tests_units',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
