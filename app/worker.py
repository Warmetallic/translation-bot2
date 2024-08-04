import pika
from utils.rabbitmq import consume_messages


def process_translation(ch, method, properties, body):
    text = body.decode()
    # Perform translation logic here
    print(f"Translating text: {text}")


if __name__ == "__main__":
    consume_messages("translate_queue", process_translation)
