import json

import pika
"""
RabbitMQ is a messaging broker - an intermediary for messaging.
It gives your applications a common platform to send and receive messages, 
and your messages a safe place to live until received
"""

def task(body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='send_mail')

    channel.basic_publish(exchange='',
                     routing_key='send_mail', 
                     body=json.dumps(body)
                     )
    print(f" [x] Sent {json.dumps(body)}")
    connection.close()


