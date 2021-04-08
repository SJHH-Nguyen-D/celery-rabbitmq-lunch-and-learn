# About

This is a learning ground for the distributed task queue Celery for asychronous task distribution with our message broker - RabbitMQ in the setting of FastAPI.

Distributed task queues provided by Celery allow us to perform many asynchronous tasks efficiently via a messaging protocol to deliver and consume tasks. Celery doesn't come with it's own messenger to deliver these tasks or messages (data and computation), but relies on other third party messager 'brokers' to do the delivery work. 

There are several choices and tradeoffs with selecting a message broker but the most popular and trusted options for production grade message brokers are RabbitMQ and Redis (redis provides key-value-store, message broker, among other things). We're going with RabbitMQ today, but it is just ask easy to plug-and-play with Redis. 

We run our message broker RabbitMQ as a background process to which Celery producers enqueues the tasks and passes tasks to via a message queueing exchange protocol. RabbitMQ passes off the tasks from the queue to availble celery workers who in turn, consume the tasks (run the function or computation) and return an asynchronous result +/- storing it in a backend (database of your choice).

![Celery RabbitMQ Diagram](https://i.pinimg.com/originals/f8/fa/40/f8fa40a9419f4e264563ef577a9e2777.png)


# Setup

You'll need:

    * rabbitmq
        * docker pull rabbitmq 
    * celery
        * `pip install celery`
        * `sudo apt-get install python-celery-common`
    * fastapi
	* `pip install fastapi`


# Running

Step by step we'll go through how each of the parts of the application are setup and communicate with one another.

## RabbitMQ - The Message Broker

RabbitMQ can be run as in a server as a background process for which we can pass tasks to from our API, in this case it's a FastAPI app.

We retrieve the image for RabbitMQ with:

    docker pull rabbitmq

We can also assign this as our broker service when we docker-compose our application together.


### Celery

We define a Celery worker module `worker.py` which contains our Celery worker application.

To define our celery worker application to be the task queuing god that it is, we define some important parameters such as:

    broker: url of our broker, i.e RabbitMQ service
    backend: url of our backend; optional if don't want to store the results of your consumed tasks

We build out our celery service from our `Dockerfile` first with:

	docker build -t celery_simple:latest .

Docker starts and runs the Celery worker process which starts a task queue to prepare to send messages/tasks to the task broker RabbitMQ

Run the celery background process with:

    celery -A worker.app worker --loglevel=info

The `-A` flag indicates the application name (`worker.app`) that we want to start and we specify to start a worker. The `--loglevel` flag indicates a log-level of `info`


## Docker-Composing everything Together
The end product can be spun up (rabbitmq in the background, celery worker running, fastapi app with consumer) with:

    docker-compose up

Visit `localhost:8080/docs` to visit the automatic interactive documentation rendered by Swagger UI as part of FastAPI



## Forwarding tasks into Celery task queue

Now that you have both a RabbitMQ server and celery process running in the background, in a different shell, you'll want to test out whether or not the process works. We can do this with the python REPL. We run our celery-wrapped function as a celery `task`. Initially we just get the function to run as per normal, but if we want to pass the task to the celery task queue, we can call `my_celery_wrapped_func.delay(arg1)`. We can see attributes from this asynchronous task object such as `.status`. If we want to get the result we can call the `.get()` method.

# Resources

[Asynchronous Tasks in Python  with Celery 2020](https://www.youtube.com/watch?v=THxCy-6EnQM) 

[RabbitMQ server setup with docker-compose](https://codeburst.io/get-started-with-rabbitmq-on-docker-4428d7f6e46b)
