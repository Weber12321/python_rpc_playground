import pika
import os
import sys
import time


def main():
    """
    + https://www.rabbitmq.com/tutorials/tutorial-one-python.html
    + https://www.rabbitmq.com/tutorials/tutorial-two-python.html

    ### Round-robin dispatching

    By default, RabbitMQ will send each message to the next consumer,
    in sequence. On average every consumer will get the same number
    of messages. This way of distributing messages is called `round-robin`.
    Try this out with three or more workers.


    ### Message acknowledgment

    Doing a task can take a few seconds, you may wonder what happens
    if a consumer starts a long task and it terminates before it completes.
    With our current code once RabbitMQ delivers message to the consumer,
    it immediately marks it for deletion. In this case,
    if you terminate a worker, the message it was just processing is lost.
    The messages that were dispatched to this particular worker but were
    not yet handled are also lost.

    In order to make sure a message is never lost, RabbitMQ supports message
    acknowledgments. An ack(nowledgement) is sent back by the consumer to
    tell RabbitMQ that a particular message had been received, processed and
    that RabbitMQ is free to delete it.{

    If a consumer dies (its channel is closed, connection is closed,
    or TCP connection is lost) without sending an ack, RabbitMQ will understand
     that a message wasn't processed fully and will re-queue it. If there are
     other consumers online at the same time, it will then quickly redeliver it
      to another consumer. That way you can be sure that no message is lost,
      even if the workers occasionally die.

    To debug with forgotten acknowledgment, try:
    `rabbitmqctl list_queues name messages_ready messages_unacknowledged`
    in the terminal.

    ### Message durability

    When RabbitMQ quits or crashes it will forget the queues and messages
    unless you tell it not to. Two things are required to make sure
    that messages aren't lost: we need to mark both the queue and messages
    as durable.

    ### Fair dispatch

    

    """

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # https://pika.readthedocs.io/en/latest/modules/parameters.html#connectionparameters
    credentials = pika.PlainCredentials('user', 'password')
    parameters = pika.ConnectionParameters(
        'localhost', 5672, '/', credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # We don't need to declare again if you are sure the queue was declared
    # at the tasks.py and it was executed. This is just to make sure.
    # or using `rabbitmqctl list_queues` to check the queue in terminal.
    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_consume(queue='hello',
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

