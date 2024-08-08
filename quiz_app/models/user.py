from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from ..manager import UserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(_("username"), max_length=15,unique=True)
    email = models.EmailField(_("email"),unique=True)
    is_superuser = models.BooleanField(_("is_superuser"),default=False)
    is_validate = models.BooleanField(_("is_validate"),default=False)
    is_staff = models.BooleanField(_("is_staff"),default=False)
    user_create_time = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)
    last_login = models.DateTimeField(_(""), auto_now=True, auto_now_add=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
    
