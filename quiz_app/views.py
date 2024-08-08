from django.utils import timezone
from datetime import timedelta
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .utils import generate_otp,send_email
from .models.otp import otp_class
from .models.user import User
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
        return Response({"user":user,"otp":otp_generated})
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
