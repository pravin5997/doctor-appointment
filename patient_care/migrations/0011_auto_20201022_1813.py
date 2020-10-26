# Generated by Django 3.1.2 on 2020-10-22 12:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_care', '0010_bookdoctor_availabilty_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availabilty_type', models.CharField(choices=[('Telemedicine', 'Telemedicine'), ('In-Person', 'In-Person')], default='Telemedicine', max_length=15)),
                ('person_consultation_type', models.CharField(choices=[('Emergency', 'Emergency'), ('Regular', 'Regular')], max_length=10)),
                ('emergency_details', models.TextField(blank=True, null=True)),
                ('ambulance', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PreferredDoctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_is_preferred', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_user', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='confirmbooking',
            name='book',
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='specialization',
            field=models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Endocrinologists', 'Endocrinologists'), ('GUN', 'Nephrologists')], max_length=18),
        ),
        migrations.DeleteModel(
            name='BookDoctor',
        ),
        migrations.DeleteModel(
            name='ConfirmBooking',
        ),
    ]