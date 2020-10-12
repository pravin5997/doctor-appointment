from django.contrib import admin
from .models import User, PatientProfile, DoctorProfile, BookDoctor, SearchAttribute, SearchAttributeValue
# Register your models here.
admin.site.register(User)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(BookDoctor)
admin.site.register(SearchAttribute)
admin.site.register(SearchAttributeValue)