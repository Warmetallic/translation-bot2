import pika
from decouple import config
import logging

logging.basicConfig(level=logging.DEBUG)


def get_connection():
    rabbitmq_host = config("RABBITMQ_HOST")
    logging.debug(f"Connecting to RabbitMQ host: {rabbitmq_host}")
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
    return connection


def publish_message(queue, message):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange="", routing_key=queue, body=message)
    connection.close()


def consume_messages(queue, callback):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
