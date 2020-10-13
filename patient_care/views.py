from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from .serializers import SignupSerializer, PatientProfileSerializer, DoctorSerializer, AttributeSerializer, DoctorBookSerializer, LoginSerializer, ConformBookingSerializer
from rest_framework import status, viewsets
from .models import User,PatientProfile, DoctorProfile, SearchAttribute, BookDoctor, ConformBooking
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.permissions import IsAuthenticated



def home(request):
    return HttpResponse("welcome to new project start")


class Register(APIView):
    serializer_class = SignupSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            
            curent_site = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.id))
            email = EmailMessage(
                "email verification", "Please click on the link to veryfr your email, http://"+curent_site+"/activate/"+uid+"/"+token,settings.EMAIL_HOST_USER, to=[user.email]
            )
            email.send(fail_silently=False)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerification(APIView):

    def get(self, request, uidb64, token, format=None):
     
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"Success": "Congratulations your email verification has been successfully completed"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"Success": LoginSerializer(user).data}, status=status.HTTP_200_OK)
        return Response({"Failed":"invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)


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
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchAttributeList(ListCreateAPIView):
    queryset = SearchAttribute.objects.all()
    serializer_class = AttributeSerializer


class SearchDoctor(APIView):

    def get(self, request, search, format=None):
        obj = DoctorProfile.objects.filter(Q(location__icontains=search)| Q(hospital__icontains=search))
        serializer = DoctorSerializer(obj, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchFilterDoctor(APIView):

    def get(self, request, search, attribute, format=None):
        obj = DoctorProfile.objects.filter(Q(location__icontains=search)| Q(hospital__icontains=search))
        filter_object = obj.filter(experience__icontains=attribute)
        serializer = DoctorSerializer(filter_object, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorBook(ListCreateAPIView):
    queryset = BookDoctor.objects.all()
    serializer_class = DoctorBookSerializer


class ConformBookingDoctor(ListCreateAPIView):
    queryset = ConformBooking.objects.all()
    serializer_class = ConformBookingSerializer