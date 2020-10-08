from django.db import models
from django.contrib.auth.models import (AbstractBaseUser)
from .managers import UserManager
from django.db.models.signals import post_save
import signal

class Patient(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=55,unique=True)
    mobile = models.CharField(max_length=15)
    referral_code = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile','username',"referral_code"]

    def __str__(self):
        return self.email

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
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
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
    habits = models.CharField(max_length=55)
    physical_activity = models.CharField(max_length=55)
    pre_existing_disease = models.CharField(max_length=55)
    prior_surgeries_type = models.CharField(max_length=8, choices=SURGERY_TYPE)
    prior_surgeries_year = models.IntegerField()
    allergies = models.CharField(max_length=50)
    report = models.ImageField(upload_to='patient/', blank= True, null = True)
    

class Doctor(models.Model):
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

    name = models.CharField(max_length=55)
    photo = models.ImageField(upload_to="doctor/")
    hospital = models.CharField(max_length=55)
    specialization = models.CharField(max_length=18, choices=SPECIALIZATION_TYPE)
    experience = models.IntegerField()
    degree = models.CharField(max_length=50)
    language = models.CharField(max_length=1, choices=LANGUAGE)
    location = models.CharField(max_length=50)
 
    def __str__(self):
        return self.name

class BookDoctor(models.Model):
    AVAILABILITY_TYPE = (
            ("Telemedicine", "Telemedicine"),
            ("In-Person", "In-Person"),
    )
    CONSULTATION_TPYE = (
        ("Emergency", "Emergency"),
        ("Regular", "Regular"),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="booking_patient")
    doctor = models.ForeignKey(Doctor, related_name="booking_doctor", on_delete=models.CASCADE)
    doctor_is_preferred = models.BooleanField(default=False)
    availabilty_type = models.CharField(max_length=15, choices=AVAILABILITY_TYPE)
    person_consultation_type = models.CharField(max_length=10, choices=CONSULTATION_TPYE)
    emergency_details = models.TextField(blank=True, null=True)
    ambulance = models.BooleanField(default=False)

    def __str__(self):
        return "doctor - {}".format(self.doctor.name)
  

class SearchAttribute(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class SearchAttributeValue(models.Model):
    attribute = models.ForeignKey(SearchAttribute, related_name="search_attribute", on_delete= models.CASCADE)
    value = models.CharField(max_length=15)


class ConformBooking(models.Model):
    book = models.ForeignKey(BookDoctor, related_name="conform_booking", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "{}".format(self.id)
    
