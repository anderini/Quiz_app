import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    otp=""
    for i in range(0,4,1):
        otp+=str(random.randint(0,9))
    return otp

def send_email(email,otp):
    subject = 'Quiz App'
    message = f'QuizApp Doğrulama kodunuz : {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_email = [email,]
    send_mail(subject,message,email_from,recipient_email)