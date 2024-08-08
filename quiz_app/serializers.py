from rest_framework import serializers
from .models.user import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from rest_framework.exceptions import AuthenticationFailed

class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(validators=[validate_password])
    class Meta:
        model=User
        fields=['email','password','username','id']      
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user