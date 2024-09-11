from rest_framework import serializers
from .models.user import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext_lazy as _

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User

        extra_kwargs = {
            "username":{
                "error_messages": {
                    "max_length": _('Kullanıcı adı 15 karakterden büyük olamaz!'),
                    "blank":"Kullanıcı adı kısmı boş bırakılamaz!",
                },
                "validators": [
                    MinLengthValidator(4, message=_('Kullanıcı adı en az 4 karakter olmalıdır!')),
                    MaxLengthValidator(15, message=_('Kullanıcı adı 15 karakterden büyük olamaz!')),
                    UniqueValidator(
                            queryset=User.objects.all(),
                            message=_("Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı seçin.")
                    )
                ]
            },    
            "email": {
                "error_messages": {
                    "blank":"Email kısmı boş bırakılamaz!"
                },
                "validators": [
                    UniqueValidator(
                            queryset=User.objects.all(),
                            message=_("Bu email zaten kullanılıyor. Lütfen başka bir email kullanın.")
                    )
                ]
            },
            "password": {
                'write_only': True,
                'validators': [
                    MinLengthValidator(8, message=_('Parola en az 8 karakter olmalıdır!')),
                    MaxLengthValidator(128, message=_('Parola en fazla 128 karakter olabilir!')),
                ],
                'error_messages': {
                    'blank': 'Parola kısmı boş bırakılamaz!',
                }
            }
        }

        fields=['email','password','username','id']
    def validate_password(self, value):
        if value.isdigit():
            raise serializers.ValidationError(_('Parola tamamen sayılardan oluşamaz!'))
        return value
    def validate_username(self, value):
        if ' ' in value:
            raise serializers.ValidationError(_("Kullanıcı adı boşluk karateri içeremez!"))
        return value    
    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        return user
  
class UserLoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,error_messages={
        'blank': 'Şifre Boş Bırakılamaz.',
    })
    username=serializers.CharField(error_messages={
        'blank': 'Kullanıcı Adı Boş Bırakılamaz.',
    })
    class Meta:
        model=User
        fields=['password','username','id']
    def create(self,validated_data):
        raise NotImplementedError(".")

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password=serializers.CharField(write_only=True)
    new_password=serializers.CharField(validators=[validate_password],write_only=True)
    confirm_password=serializers.CharField(write_only=True)

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
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(validators=[validate_password],write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Password doesn't match")
        return attrs
    
class DeleteUserSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
     
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        user = self.context['request'].user
        if not user.check_password(password):
            raise serializers.ValidationError("Mevcut şifre geçersiz.")
        if password != confirm_password:
            raise serializers.ValidationError("Password doesn't match")
        return attrs