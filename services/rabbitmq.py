import pika
import json


def get_connection():
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
    return connection


def publish_message(payload: dict, queue: str):
    """
    Publica un mensaje en la cola de RabbitMQ.
    payload debe incluir: action, task_id y los datos necesarios.
    """
    try:
        connection = get_connection()
        channel = connection.channel()

        channel.exchange_declare(exchange='orders', exchange_type='direct')

        channel.basic_publish(
            exchange="orders",
            routing_key=queue,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,  # mensaje persistente
                content_type="application/json"
            )
        )

        print("Petición publicada en el exchange")
        connection.close()

    except Exception as e:
        print(f"Failed to publish message: {e}")
        raise