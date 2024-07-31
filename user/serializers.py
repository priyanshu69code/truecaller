# serializers.py

from rest_framework import serializers
from user.models import User
from phonenumber_field.serializerfields import PhoneNumberField


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={
                                      'input_type': 'password'})
    number = PhoneNumberField()

    class Meta:
        model = User
        fields = ['number', 'password', 'password2',
                  'email', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            number=validated_data.get('number', None),
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class OTPRequestSerializer(serializers.Serializer):
    number = PhoneNumberField()

    def validate(self, data):
        return data


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    number = PhoneNumberField()

    def validate(self, data):
        return data
