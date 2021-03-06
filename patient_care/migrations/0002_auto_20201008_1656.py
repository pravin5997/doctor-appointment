# Generated by Django 3.1.2 on 2020-10-08 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_care', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdoctor',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_doctor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bookdoctor',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_patient', to=settings.AUTH_USER_MODEL),
        ),
    ]
