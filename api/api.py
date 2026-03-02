from fastapi import FastAPI, Depends, status, HTTPException

app = FastAPI()


## inicializar la base de datos
from database.conn import engine, get_db
from database.models import Base, Task, Order
from .schemas import *

Base.metadata.create_all(bind=engine)

print("---- Base de datos inicializada ----")


## funcion para publicar en cola
from services.rabbitmq import publish_message


#______________ Tasks _________________
def crearTask(db, taskType):
    task = Task(status="Pending", type=taskType)

    db.add(task)
    db.flush()
    task_id = task.task_id
    db.commit()
    return task_id

@app.get("/tasks")
def list_tasks(db = Depends(get_db)):
    return db.query(Task).order_by(Task.task_id.desc()).all()

@app.get("/tasks/{task_id}")
def get_task(task_id: int, db = Depends(get_db)):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task



#________________  Orders ________________

@app.get("/orders")
def list_orders(db = Depends(get_db)):
    return db.query(Order).order_by(Order.order_id.desc()).all()

@app.post("/orders", status_code=status.HTTP_202_ACCEPTED)
def createOrder(payload: OrderCreate, db = Depends(get_db)):
    task_id = crearTask(db, "Create")

    publish_message({
        "action": "create",
        "task_id": task_id,
        "product": payload.product,
        "product_quantity": payload.product_quantity
    }, 'create_q')
    
    return AcceptedResponse(task_id=task_id)

@app.delete("/orders/{order_id}", status_code=status.HTTP_202_ACCEPTED)
def deleteOrder(order_id: int, db = Depends(get_db)):
    order = db.get(Order, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    task_id = crearTask(db, "Delete")

    publish_message({
        "action": "delete",
        "task_id": task_id,
        "order_id": order_id
    }, 'delete_q')
    
    return AcceptedResponse(task_id=task_id)
