from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError) and response is not None:
        # Tüm hata mesajlarını toplayıp tek bir string haline getirme
        messsage = ""
        for error_list in response.data.items():
            messsage+= error_list[1][0]
        
        # Hata mesajını tek bir string içinde döndürme
        response.data = {
            'message': messsage,
            'status': False,
            'otp': " ",
            'userId': " ",
        }

    return response