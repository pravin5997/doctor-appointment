from .models import User, PatientProfile, DoctorProfile, SearchAttribute, BookDoctor, ConformBooking
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', "first_name", "last_name",'email', "user_type", 'referral_code', "mobile", "password")

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
    
    class Meta:
        model = PatientProfile
        fields = "__all__"
        read_only_fields = ("user",)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = "__all__"
        read_only_fields = ("user",)
        

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchAttribute
        fields = "__all__"


class DoctorBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDoctor
        fields = "__all__"

class ConformBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConformBooking
        fields = "__all__"