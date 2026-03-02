# Orders Stream Processor
## General description
This project is an asynchronous order processing system that uses RabbitMQ as a messaging broker, based on Asynchronous Request-Reply pattern. The project allows queuing order publishing and deletion tasks, which are processed asynchronously by dedicated workers, thereby decoupling the business logic from the execution of operations on the database.

The general flow is as follows:
1. A client sends requests to the REST API (FastAPI).
2. Order creation or deletion operations are published as messages to RabbitMQ queues.
3. Workers consume the messages from the queue and execute the corresponding operations on the PostgreSQL database asynchronously.

## Architecture
(image will go here)

## Deployment with Docker Compose
### Prerequisites
* [Docker](https://www.docker.com/) installed
* [Docker compose](https://docs.docker.com/compose/) installed

### Steps
1. **Clone the repository**
```console
git clone https://github.com/jpovalles/Orders-Stream-Processor.git
cd Orders-Stream-Processor
```

2. **Start the services:**
```console
docker compose up --build
```

3. **Verify container status:**

It is recommended to review the container logs to confirm that all services have started correctly and that the workers are connected to RabbitMQ:

(image will go here)

Make sure there are no connection errors between services before running the client.

## Running the client
Once all containers are running correctly, execute the clients.py script inside the python_client container to simulate sending orders to the queue:
```console
docker exec -it python_service python clients.py
```

When you run `clients.py`, use the menu:

1. List tasks

   * Option `1`
   * Useful for viewing the tasks created by asynchronous operations.

2. View a task by ID

   * Option `2`
   * Enter the numeric `task_id` when prompted.

3. List orders

   * Option `3`
   * Displays all orders stored in the database.

4. Create order

   * Option `4`
   * Enter:

     * `Product` (text)
     * `Quantity` (integer)
   * This sends the order to the API and typically enqueues the processing in RabbitMQ.

5. Delete order

   * Option `5`
   * Enter the numeric `order_id`
   * Confirm with `s` to proceed.

6. Exit

   * Option `0`

## API Documentation

The API documentation is available at:

`http://localhost:8001/docs`

If you are accessing the API from within the Docker network (e.g., from another container), the base URL would be:

`http://api:8001`
