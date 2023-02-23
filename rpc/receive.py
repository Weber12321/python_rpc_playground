import pika
import os
import sys

def main():
    """
    https://www.rabbitmq.com/tutorials/tutorial-one-python.html

    """
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # https://pika.readthedocs.io/en/latest/modules/parameters.html#connectionparameters
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters(
        'localhost', 5672, '/', credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # We don't need to declare again if you are sure the queue was declared
    # at the send.py and it was executed. This is just to make sure.
    # or using `rabbitmqctl list_queues` to check the queue in terminal.
    channel.queue_declare(queue='hello')

    channel.basic_consume(queue='hello',
                          auto_ack=True,
                          on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

