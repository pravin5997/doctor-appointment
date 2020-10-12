from django.urls import path, include
from .views import home, Register, LoginView, PatientProfileView, DoctorProfileView, SearchAttributeList, SearchDoctor, SearchFilterDoctor, DoctorBook, ConformBookingDoctor, EmailVerification
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"patient", PatientProfileView, basename="patient_profile")
router.register(r"doctor", DoctorProfileView, basename="doctor_details")


urlpatterns = [
    path("", home, name="home"),
    path('', include(router.urls)),
    path("register/", Register.as_view(), name="register"),
    path("login/", LoginView.as_view(), name= "login"),
    path("attribute/", SearchAttributeList.as_view(), name="attribute"),
    path("book/", DoctorBook.as_view(), name="booking"), 
    path("search/<str:search>/", SearchDoctor.as_view(), name= "search"),
    path("search/<str:search>/<str:attribute>/", SearchFilterDoctor.as_view(), name="doctor_filter"),
    path('conform-booking', ConformBookingDoctor.as_view(), name="conform_booking"),
    path("activate/<uidb64>/<token>/", EmailVerification.as_view(), name = "verify_email"),
]