import pika
import sys


def send_request(body:str) -> None:
    """
    https://www.rabbitmq.com/tutorials/tutorial-one-python.html
    https://www.rabbitmq.com/tutorials/tutorial-two-python.html

    """

    # https://pika.readthedocs.io/en/latest/modules/parameters.html#connectionparameters
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters(
        'localhost', 5672, '/', credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(exchange='',
                          routing_key="task_queue",
                          body=body,
                          properties=pika.BasicProperties(
                              delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                          ))
    print(f" [x] Sent {body}")
    connection.close()


if __name__ == '__main__':
    input = ' '.join(sys.argv[1:]) or 'Hi, Weber!'
    send_request(input)
