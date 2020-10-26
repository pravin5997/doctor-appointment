from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from .serializers import UserSerializer, PatientProfileSerializer, DoctorProfileSerializer, DoctorAppointmentSerializer, LoginSerializer
from rest_framework import status, viewsets
from .models import User,PatientProfile, DoctorProfile, Appointment
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication


def home(request):
    return HttpResponse("welcome to new project start")

class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class Register(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user_id = User.objects.latest('id')
            user = serializer.save(universal_id = 10000000 + user_id.id + 1)
            token = Token.objects.create(user=user)
            curent_site = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.id))
            email = EmailMessage(
                "email verification", "Please click on the link to veryfr your email, http://"+curent_site+"/activate/"+uid+"/"+token.key,settings.EMAIL_HOST_USER, to=[user.email]
            )
            email.send(fail_silently=False)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerification(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token, format=None):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        token = Token.objects.get(user=user)
        if user is not None and token:
            user.is_active = True
            user.save()
            email = EmailMessage("success message",
                "Congratulations your email verification has been successfully completed.your upc id is "+user.universal_id+", click here to login, http://127.0.0.1:8000/login/",settings.EMAIL_HOST_USER, to=[user.email]
            )
            email.send(fail_silently=False)
            return Response({"Success": "Congratulations your email verification has been successfully"},status=status.HTTP_201_CREATED)
        return Response({"error": "faild to conform email"},status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({'token': token.key},status=status.HTTP_200_OK)


class PatientProfileView(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorProfileView(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
   
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchDoctor(APIView):

    def get(self, request, format=None):
        user_list = []
        search = request.GET.get("search", None)
        sort_by = request.GET.get("sort_by", None)
        if search == "1":
            user_list = list(Appointment.objects.filter(patient=request.user).values_list("doctor_id", flat=True).order_by("date_time"))
        else:
            user_list = list(User.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search)).values_list("id", flat=True))
        obj = DoctorProfile.objects.filter(Q(user_id__in=user_list) | Q(location__icontains=search) | Q(hospital__icontains=search) | Q(specialization__icontains=search))
        if sort_by:
            sort_obj = obj.order_by(sort_by)
        else:
            sort_obj = obj
        serializer = DoctorProfileSerializer(sort_obj, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorAppointment(ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = DoctorAppointmentSerializer
