from rest_framework import serializers
from .models.user import User
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
  
class UserLoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField()
    username=serializers.CharField()
    email=serializers.EmailField()

    class Meta:
        model=User
        fields=['email','password','username','id',]

    def create(self,validated_data):
        raise NotImplementedError(".")

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password=serializers.CharField()
    new_password=serializers.CharField(validators=[validate_password])
    confirm_password=serializers.CharField()

    class Meta:
        model=User
        fields=['new_password','confirm_password','old_password']

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        old_password = attrs.get('old_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Password doesn't match")

        user = self.context['request'].user

        if not user.check_password(old_password):
            raise serializers.ValidationError("Mevcut şifre geçersiz.")
        
        return attrs
    
    def create(self,validated_data):
        raise NotImplementedError(".")
    
    def update(self,instance ,validated_data):
        new_password = validated_data.get('new_password')
        instance.set_password(new_password)
        instance.save()
        return instance
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_password = serializers.CharField(validators=[validate_password])

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Password doesn't match")
        return attrs