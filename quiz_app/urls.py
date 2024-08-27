from django.urls import path
from .views import register_user,verify_user,login_user,manual_token_refresh,change_password,request_reset_password,reset_password,logout_user,delete_user

urlpatterns = [
    path('register', register_user,name='register'),
    path('verifyUser', verify_user,name='verifyUser'),
    path('login', login_user,name='login'),
    path('refresh_token', manual_token_refresh,name='manuel token refresh'),
    path('changepassword', change_password,name='change password'),
    path('requestresetpassword', request_reset_password,name='request reset password'),
    path('resetpassword/<uid64>/<token>', reset_password,name='password reset'),
    path('logout', logout_user,name='logout'),
    path('deleteuser', delete_user,name='delete user'),

]