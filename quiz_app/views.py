from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from .serializers import UserRegisterSerializer,UserLoginSerializer,ChangePasswordSerializer,PasswordResetRequestSerializer,PasswordResetSerializer,DeleteUserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .utils import generate_otp,send_email
from .models.otp import otp_class
from .models.user import User
from .models.reset_password import request_reset_password_class
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your views here.
@api_view(['POST'])
def register_user(request):
    otp_expiry=timezone.now() + timedelta(minutes=5) #expires in 5 minute
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user=serializer.data
        otp_generated=generate_otp()
        otp_class.objects.create(otp=otp_generated,user_id=user['id'],otp_expiry=otp_expiry)
        send_email(email=user['email'],otp=otp_generated)
        return Response({"otp":otp_generated,"userID":user['id'],"status":True,"message":"Başarıyla Kayıt Olundu."})
    
@api_view(['POST'])
def verify_user(request):
    isMatch = request.data['isMatch']
    userID = request.data['userID']
    if isMatch == True:
        User.objects.filter(id=userID).update(is_validate=True)
        otp_class.objects.filter(user_id=userID).delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = authenticate(username=serializer.data['username'],password=serializer.data['password'])
        if not user:
           raise AuthenticationFailed("authentication failed!!")
        else:
            if user.is_validate != 1:
                raise AuthenticationFailed("email not verified!!")
            else:
                token=user.tokens()
                return Response({
                    "access_token":str(token.get('access')),
                    "refresh_token":str(token.get('refresh')),
                })
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def manual_token_refresh(request):
    refresh_token = request.data.get('refresh')

    try:
        # Refresh token'ı doğrula ve access token'ı al
        refresh = RefreshToken(refresh_token)
        return Response({
            'access': str(refresh.access_token),
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request':request})
    if serializer.is_valid(raise_exception=True):
        serializer.instance = request.user
        serializer.save() #ChangePasswordSerializer icindeki update metodunu cagirmak icin
        return Response({'message': 'Change Password Succesfully.'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def request_reset_password(request):
    serializer = PasswordResetRequestSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        token_expiry = timezone.now() + timedelta(minutes=5) #expires in 5 minute
        token_object = request_reset_password_class.objects.create(user_id=user.id,token=token,token_expiry=token_expiry)
        token_object.save()
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        resetpassword_url = f"resetpassword/{encoded_pk}/{token}"
        print(resetpassword_url)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def reset_password(request,uid64,token):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        pk = urlsafe_base64_decode(uid64)
        try:
            reset_password_object = request_reset_password_class.objects.get(token=token,user_id=pk)
        except request_reset_password_class.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not reset_password_object:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.get(id=pk)
            user.set_password(serializer.data['new_password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()  # Token'ı geçersiz kıl
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    serializer = DeleteUserSerializer(data=request.data, context={'request':request})
    if serializer.is_valid(raise_exception=True):
        user = request.user
        user.delete()
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()  # Token'ı geçersiz kıl
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)