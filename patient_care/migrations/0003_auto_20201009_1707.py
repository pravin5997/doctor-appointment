# Generated by Django 3.1.2 on 2020-10-09 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_care', '0002_auto_20201008_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=55),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=55),
        ),
    ]