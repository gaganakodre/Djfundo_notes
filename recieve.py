import json
import os
import smtplib
import sys

import pika


class Consumer:

    def send_mail(self, body):
        EMAIL_ADDRESS = os.getenv('EMAIL_HOST_USER')
        EMAIL_PASSWORD = os.getenv('EMAIL_HOST_USER')

        data = json.loads(body)
        print(data)
        receivers = [data.get('email')]
        subject = "Verification"
        body = "Click on this " + data.get('message')
        message = f'subject: {subject}\n\n{body}'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, receivers, message)
        server.close()

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='send_mail')

        def callback(ch, method, properties, body):
            self.send_mail(body)
            print(" [x] Received %r" % body)

        channel.basic_consume(queue='send_mail', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


if __name__ == '__main__':
    try:
        Consumer().run()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
