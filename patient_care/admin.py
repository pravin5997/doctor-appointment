from django.contrib import admin
from .models import Patient, PatientProfile, Doctor, BookDoctor, SearchAttribute, SearchAttributeValue
# Register your models here.
admin.site.register(Patient)
admin.site.register(PatientProfile)
admin.site.register(Doctor)
admin.site.register(BookDoctor)
admin.site.register(SearchAttribute)
admin.site.register(SearchAttributeValue)