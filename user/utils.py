from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.reverse import reverse

from user.token import JWT


class Util:
    @staticmethod
    def send_email(data):  # user.utils.Util.send_emai
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
