import pika


def send_request(body:str) -> None:
    """
    https://www.rabbitmq.com/tutorials/tutorial-one-python.html

    """

    # https://pika.readthedocs.io/en/latest/modules/parameters.html#connectionparameters
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters(
        'localhost', 5672, '/', credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=body)
    print(" [x] Sent 'Hello World!'")
    connection.close()


if __name__ == '__main__':
    send_request('Hi, Weber!')