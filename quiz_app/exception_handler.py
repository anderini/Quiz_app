from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from .serializers import UserRegisterSerializer

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError) and response is not None:
         # Context'teki view üzerinden serializer'ı al
        view = context.get('view')
        
        messsage = ""
        for error_list in response.data.items():
            messsage+= error_list[1][0]
        
        # Hata mesajını tek bir string içinde döndürme
        if view.__class__.__name__ == 'register_user':
            response.data = {
                'message': messsage,
                'status': False,
                'otp': "",
                'userID': -1,
            }
        elif view.__class__.__name__ == 'login_user':
             response.data = {
                "accessToken":"",
                "refreshToken":"",
                "userID":-1,
                "username":"",
                "password":"",
                "email":"",
                "createdAt":"",
                "lastOnlineAt":"",
            }

    return response