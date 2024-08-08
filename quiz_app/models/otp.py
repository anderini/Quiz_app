from django.db import models
from .user import User

class otp_class(models.Model):
    otp= models.CharField(max_length=6,unique=True)
    otp_expiry=models.DateTimeField(null=True,blank=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    otp_max_out=models.IntegerField(default=2)