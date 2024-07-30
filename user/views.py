from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from user.models import User, OTP
from .serializers import UserRegistrationSerializer, OTPRequestSerializer, VerifyOTPSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .utils import generate_otp
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful. Please verify your email.'}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data['number']
            try:
                user = User.objects.get(number=number)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist.'}, status=HTTP_400_BAD_REQUEST)

            if user.is_verified:
                return Response({'error': 'User is already verified.'}, status=HTTP_400_BAD_REQUEST)

            # Check if there's a non-expired OTP for the user
            otp_instance = OTP.objects.filter(
                user=user).order_by('-created_at').first()
            if otp_instance and not otp_instance.is_expired():
                # Send the same OTP again
                otp_instance.send_otp()
                return Response({'message': 'OTP sent successfully.'}, status=HTTP_200_OK)
            elif otp_instance and otp_instance.is_expired():
                # Delete the expired OTP
                otp_instance.delete()

            # Generate a new OTP
            otp = generate_otp()
            otp_instance = OTP.objects.create(
                user=user, otp=otp)
            otp_instance.send_otp()
            return Response({'message': 'OTP sent successfully.'}, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data['number']
            try:
                user = User.objects.get(number=number)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist.'}, status=HTTP_400_BAD_REQUEST)
            otp_instance = OTP.objects.filter(
                user=user).order_by('-created_at').first()
            if otp_instance.is_valid(serializer.validated_data["otp"]):
                user.is_verified = True
                otp_instance.delete()
                user.save()
                return Response({'message': 'OTP verified successfully.'}, status=HTTP_200_OK)
            return Response({'error': 'Invalid OTP.'}, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(number=request.data['number'])
        if not user.is_verified:
            return Response({'error': 'User is not verified.'}, status=HTTP_400_BAD_REQUEST)
        return response
