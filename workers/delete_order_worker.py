import pika

import json
from sqlalchemy.orm import Session
from database.conn import SessionLocal
from workers.worker import update_task_status
from database.models import Task, Order

import logging

from services.rabbitmq import get_connection

logging.basicConfig(level=logging.INFO)

def handle_delete(db: Session, data: dict):
    order = db.query(Order).filter(Order.order_id == data["order_id"]).first()
    if order:
        db.delete(order)
        db.commit()
        logging.info(f"Order deleted: {data['order_id']}")
    else:
        raise ValueError(f"Order {data['order_id']} not found for delete")


def callback(ch, method, properties, body):
    db = SessionLocal()
    task_id = None
    try:
        data = json.loads(body)
        task_id = data["task_id"]
        action = data["action"]

        logging.info(f"{method.routing_key} Received message | action={action} | task_id={task_id}")
        handle_delete(db, data)
        update_task_status(db, task_id, 'Completed')

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logging.error(f"Error processing message: {e}")
        if task_id:
            update_task_status(db, task_id, 'Failed')
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    finally:
        db.close()


def main():
    connection = get_connection()
    channel = connection.channel()

    exchange_name = 'orders'
    queue_name = 'delete_q'

    # Se crea/conecta al exchange
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

    channel.queue_declare(queue=queue_name, durable=True)

    channel.queue_bind(exchange=exchange_name, queue=queue_name)
    logging.info(' [*] Esperando por eliminación de ordenes. To exit press CTRL+C')


    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

    channel.start_consuming()


if __name__ == "__main__":
    main()





