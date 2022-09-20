import logging
from time import sleep

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.reverse import reverse

logging.basicConfig(filename='fundoo_note.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()

@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@shared_task()
def email_sender(token, recipient):
    """
    Function to send the mail  using celery
    """
    try:
        sleep(10)
        send_mail(subject='Notes Registration verification with Celery',
                  message=settings.BASE_URL + reverse('verify', kwargs={"token": token}),
                  from_email=None,
                  recipient_list=[recipient])
    except Exception as ex:
        logger.exception(ex)
