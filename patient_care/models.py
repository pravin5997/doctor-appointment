from django.db import models
from django.contrib.auth.models import (AbstractBaseUser)
from .managers import UserManager
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
import signal

class User(AbstractBaseUser):
    USER_TYPE = (
        ('P', "Patient"),
        ('D', "Doctor")
        )

    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    mobile = models.CharField(max_length=15)
    referral_code = models.IntegerField(null=True, blank=True)
    universal_id = models.CharField(max_length=15, null=True, blank=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPE)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "mobile","user_type", "referral_code"]

    def __str__(self):
        return "{} - {}".format(self.user_type, self.email)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class PatientProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    SURGERY_TYPE = (
            ("General", "General Surgery"),
            ("Plastic", "Plastic Surgery"),
            ("Neuro", "Neurosurgery"),   
    )
    Habits_TYPE = (
        ("Alcohol", "Alcohol"),
        ("Smoking", "Smoking"),
        ("Tobacco", "Tobacco"),
        ("None of this", "None of this"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height = models.FloatField()
    weight = models.FloatField()
    blood_group = models.CharField(max_length=10)
    address = models.TextField(max_length=200, )
    occupation = models.CharField(max_length=25)
    marital_status = models.CharField(max_length=15)
    emergency_contact_person = models.CharField(max_length=50)
    emergency_contact_relationship = models.CharField(max_length=50)
    emergency_contact_phone = models.CharField(max_length=15)
    habits = models.CharField(max_length=55 , choices=Habits_TYPE, default="None of this")
    physical_activity = models.CharField(max_length=55)
    pre_existing_disease = models.CharField(max_length=55)
    prior_surgeries_type = models.CharField(max_length=8, choices=SURGERY_TYPE)
    prior_surgeries_year = models.IntegerField()
    allergies = models.CharField(max_length=50)
    report = models.ImageField(upload_to='patient/', blank=True, null=True)


class DoctorProfile(models.Model):
    SPECIALIZATION_TYPE = (
            ("Cardiologist" , "Cardiologist"),
            ("Endocrinologists", "Endocrinologists"),
            ("Nephrologists" ,"Nephrologists"), 
        )
    LANGUAGE = (
            ("E", "English"),
            ("G", "Gujarati"),
            ("H", "Hindi"),
        )
    AVAILABILITY_TYPE = (
            ("Telemedicine", "Telemedicine"),
            ("In-Person", "In-Person"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    photo = models.ImageField(upload_to="doctor/", blank =True, null= True)
    hospital = models.CharField(max_length=55)
    specialization = models.CharField(max_length=18, choices=SPECIALIZATION_TYPE)
    availabilty_type = models.CharField(max_length=15, choices=AVAILABILITY_TYPE, default="Telemedicine")
    experience = models.IntegerField()
    degree = models.CharField(max_length=50)
    language = models.CharField(max_length=1, choices=LANGUAGE)
    location = models.CharField(max_length=50)
    

    def __str__(self):
        return self.user.first_name 
    

class BookDoctor(models.Model):
    CONSULTATION_TPYE = (
        ("Emergency", "Emergency"),
        ("Regular", "Regular"),
    )
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking_patient")
    doctor = models.ForeignKey(User, related_name="booking_doctor", on_delete=models.CASCADE)
    doctor_is_preferred = models.BooleanField(default=False)
    person_consultation_type = models.CharField(max_length=10, choices=CONSULTATION_TPYE)
    emergency_details = models.TextField(blank=True, null=True)
    ambulance = models.BooleanField(default=False)

    def __str__(self):
        return "patient is {} - doctor is {}".format(self.patient.first_name,self.doctor.first_name)


class ConformBooking(models.Model):
    book = models.ForeignKey(BookDoctor, related_name="conform_booking", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.id)
    

