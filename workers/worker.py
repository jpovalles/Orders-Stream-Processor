import pika

from services.rabbitmq import get_connection

from database.conn import get_db
from sqlalchemy.orm import Session

from database.models import Base, Task, Order

def getChannel(exchange_name, queue_name):
    # Se obtiene la conexión y se crea el canal
    connection = get_connection()
    channel = connection.channel()

    # Se crea/conecta al exchange
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

    channel.queue_declare(queue=queue_name, exclusive=True)

    channel.queue_bind(exchange=exchange_name, queue=queue_name)
    print(' [*] Esperando por creación de ordenes. To exit press CTRL+C')
    return channel

# Actualizar estado de la tarea programada
def update_task_status(db: Session, task_id: str, status: str):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if task:
        task.status = status
        db.commit()
        print(f"Task {task_id} → {status}")