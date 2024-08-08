from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

    def create_user(self,username,email,password,**extra_fields):
        if email:
            email=self.normalize_email(email)
        else:
            raise ValueError(_("an email address is required"))
        if not username:
            raise ValueError(_("an username is required"))
        email = self.normalize_email(email)
        user = self.model(username=username,email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,username,email,password,**extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_validate", True)
        extra_fields.setdefault("is_staff", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if extra_fields.get("is_validate") is not True:
            raise ValueError(_("Validate must have is_validate=True."))
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Staff must have is_staff=True."))
        self.create_user(username,email,password,**extra_fields)

        

