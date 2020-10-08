from .models import Patient, PatientProfile, Doctor, SearchAttribute, BookDoctor, ConformBooking
from rest_framework import serializers

class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Patient
        fields = ('id','email', 'username', 'referral_code', "mobile", "password")

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("email", "password",)

    
class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"

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