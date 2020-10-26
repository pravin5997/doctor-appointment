from .models import User, PatientProfile, DoctorProfile, Appointment
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', "first_name", "last_name", 'email', "user_type", 'referral_code', "mobile", "password", "universal_id")
        read_only_fields = ("universal_id",)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password",)


class PatientProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    mobile = serializers.CharField(source="user.mobile")
    report = serializers.ImageField(required=False)
   
    class Meta:
        model = PatientProfile
        exclude = ("user",)


class DoctorProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    mobile = serializers.CharField(source="user.mobile")
    
    class Meta:
        model = DoctorProfile
        exclude = ("user",)
        

class DoctorAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"