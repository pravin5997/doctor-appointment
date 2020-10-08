# Generated by Django 3.1.2 on 2020-10-07 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_care', '0008_remove_bookdoctor_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConformBooking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conform_booking', to='patient_care.bookdoctor')),
            ],
        ),
    ]
