import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue')


def task(payload, method):

    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=str(payload),
                          properties=pika.BasicProperties(method))
    print(" [x] 'Token' Sent Successfully")
    connection.close()
