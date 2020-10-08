# Generated by Django 3.1.2 on 2020-10-07 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_care', '0005_auto_20201007_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=15)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_attribute', to='patient_care.searchattribute')),
            ],
        ),
    ]