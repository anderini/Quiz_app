from django.db import models
from .user import User

class request_reset_password_class(models.Model):
    token = models.CharField(max_length=100,unique=True)
    token_expiry=models.DateTimeField(null=True,blank=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE)