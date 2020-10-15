from django.urls import path, include
from .views import home, Register, LoginView, PatientProfileView, DoctorProfileView, SearchDoctor, DoctorBook, ConformBookingDoctor, EmailVerification
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router = DefaultRouter()
router.register(r"patient", PatientProfileView, basename="patient_profile")
router.register(r"doctor", DoctorProfileView, basename="doctor_details")


urlpatterns = [
    path("", home, name="home"),
    path('', include(router.urls)),
    path("api-token-auth/", views.obtain_auth_token, name = "api_token_auth"),
    path("register/", Register.as_view(), name="register"),
    path("login/", LoginView.as_view(), name= "login"),
    path("book/", DoctorBook.as_view(), name="booking"), 
    path("search/<str:search>/", SearchDoctor.as_view(), name= "search"),
    path('conform-booking', ConformBookingDoctor.as_view(), name="conform_booking"),
    path("activate/<uidb64>/<token>/", EmailVerification.as_view(), name = "verify_email"),
]