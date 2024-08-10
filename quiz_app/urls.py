from django.urls import path
from .views import register_user,verify_user,login_user,manual_token_refresh,get_user,change_password

urlpatterns = [
    path('register', register_user,name='register'),
    path('verify', verify_user,name='verify'),
    path('login', login_user,name='login'),
    path('refresh_token', manual_token_refresh,name='manuel token refresh'),
    path('getuser', get_user,name='get_user'),
    path('changepassword', change_password,name='change password'),
]