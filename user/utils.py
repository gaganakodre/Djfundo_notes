from django.core.mail import EmailMessage
from user.token import JWT
import logging
from celery import shared_task
from django.conf import settings
from rest_framework.reverse import reverse

logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


class Util:
    @staticmethod
    @shared_task
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']]
        )
        email.send()

    @classmethod
    def user_verify_user(cls, email, id):
        token = JWT.jwt_encode({"user_id": id, "email": email})
        link = "Click on this %s%s" % (settings.BASE_URL, reverse('user:verify', kwargs={"token": token}))
        data = {
            'subject': 'Activate Your Account',
            'body': f'Hi thank you for registering verify through this link {link}',
            'to_email': email,

        }
        cls.send_email(data)

