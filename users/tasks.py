from email import message
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_mail_celery(subject:str, message:str, email_to: str ):
    email_from = "rast1ch2286@gmail.com"
    return send_mail(subject, message,
                     email_from, [email_to,])
    