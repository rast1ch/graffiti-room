from email import message
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_mail_celery(email_to: str, uuid):
    subject = "Подтверждение адресса электронной почты"
    link = f'http://localhost:8000/account/verify/{uuid}'
    message = f"Для подтвержения адресса электронной почты, нужно перейти по ссылке {link}"
    email_from = "rast1ch2286@gmail.com"
    return send_mail(subject, message,
                     email_from, [email_to,])
    