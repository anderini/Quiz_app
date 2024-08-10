from django.utils import timezone
from datetime import timedelta
from .serializers import UserRegisterSerializer,UserLoginSerializer,ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .utils import generate_otp,send_email
from .models.otp import otp_class
from .models.user import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _


# Create your views here.
@api_view(['POST'])
def register_user(request):
    otp_expiry=timezone.now() + timedelta(minutes=5) #expires in 5 minute
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user=serializer.data
        otp_generated=generate_otp()
        otp_class.objects.create(otp=otp_generated,user_id=user['id'],otp_expiry=otp_expiry)
        send_email(email=user['email'],otp=otp_generated)
        return Response({"otp":otp_generated})
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def verify_user(request):
    is_match = request.data['is_match']
    user_id = request.data['id']
    if is_match == True:
        User.objects.filter(id=user_id).update(is_validate=True)
        otp_class.objects.filter(user_id=user_id).delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    return Response({
        'message': 'Access granted',
        'user': {
            'username': user.username,
            'email': user.email
        }
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request':request})
    if serializer.is_valid(raise_exception=True):
        user = request.user
        new_password = serializer.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Change Password Succesfully.'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)