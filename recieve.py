
import pika
import json
import sys
import os
from email.message import EmailMessage
import smtplib
import os



class Consumer:
    """
     will receive messages from the queue and print them on the screen
    """
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue')

    def mail_send(self, body):
        sender = "maheshkodergowri@gmail.com"
        sender_password = "kwbtufhqzznpdngk"
        payload = json.loads(body)
        msg = EmailMessage()  # Python EmailMessage Function
        msg['From'] = sender
        msg['To'] = payload.get('recipent')
        msg['Subject'] = 'User Registration with rabbitmq'
        msg.set_content(payload.get('message'))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user=sender, password=sender_password)
            smtp.sendmail(sender, payload.get(
                'recipent'), msg.as_string())
            print("[*] Mail sent to ", payload.get('recipent'))
            smtp.quit()


    def callback(self, ch, method, properties, body):
        # self.mail_send(body)
        print("received", body)

    def run(self):

        self.channel.basic_consume(queue='task_queue', on_message_callback=self.callback,auto_ack=True)
        print("consumer started")
        self.channel.start_consuming()


if __name__ == '__main__':

    try:
       consumer= Consumer()
       consumer.run()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


