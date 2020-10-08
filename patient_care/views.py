from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from .serializers import PatientSerializer, PatientProfileSerializer, DoctorSerializer, AttributeSerializer, DoctorBookSerializer, LoginSerializer, ConformBookingSerializer
from rest_framework import status, viewsets
from django.core import serializers
from .models import PatientProfile, Patient, Doctor, SearchAttribute, BookDoctor, ConformBooking
from django.contrib.auth import authenticate, login
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated



def home(request):
    return HttpResponse("welcome to new project start")


class Register(ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


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


class Profile(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer


class DoctorCreateUpdate(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class SearchAttributeList(ListCreateAPIView):
    queryset = SearchAttribute.objects.all()
    serializer_class = AttributeSerializer


class SearchDoctor(APIView):

    def get(self, request, search, format=None):
        obj = Doctor.objects.filter(Q(location__icontains=search) | Q(name__icontains=search) | Q(hospital__icontains=search))
        serializer = DoctorSerializer(obj, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchFilterDoctor(APIView):

    def get(self, request, search, attribute, format=None):
        obj = Doctor.objects.filter(Q(location__icontains=search) | Q(name__icontains=search) | Q(hospital__icontains=search))
        filter_object = obj.filter(experience__icontains=attribute)
        serializer = DoctorSerializer(filter_object, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorBook(ListCreateAPIView):
    queryset = BookDoctor.objects.all()
    serializer_class = DoctorBookSerializer


class ConformBookingDoctor(ListCreateAPIView):
    queryset = ConformBooking.objects.all()
    serializer_class = ConformBookingSerializer