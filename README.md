# Fundo_notes

The main objective the this project is to create the backend of Notes taking app where user can add, update and delete the notes including some customization of adding color using python and django 

## Tech Stack
Tech Stack
Technology Used: Python, Django Rest Framework

[python Docs](https://docs.python.org/), python docs to refer


[Django Docs](https://docs.djangoproject.com/), here we use lot of concepts that are implemented in this project

[DRF Docs](https://www.django-rest-framework.org/), Django rest framework to implement the serializations and etc.

Concept Used: Redis, Celery, Swagger, Logger, Jinja Template, PYJWT,
custom Middlewares, Raw queries, RabbitMQ server

1.Logger:to track the events that happen when some software 
[Logging Docs](https://docs.python.org/3/howto/logging.html)

2.Redis:Redis is a open-source, in-memory database storing data as key-value pairs.here we can store the data in cache and it acts as a message broker
[Redis](https://redis.io/)but for to install and work with redis we have to Install Linux on Windows with WSL
[WSL](https://medium.com/@rhdzmota/python-development-on-the-windows-subsystem-for-linux-wsl-17a0fa1839d)

3.Swagger:for to implement in django we have to install a library called "dfr-yasg"[swagger implementation guide](https://drf-yasg.readthedocs.io/en/stable/readme.html)

4.jinja Template:
[Templates implementation guide](https://docs.djangoproject.com/en/4.1/topics/templates/)

5.Pyjwt:
[pyjwt implementation guide](https://pyjwt.readthedocs.io/en/latest/usage.html)

6.Custom Middleware:
[implementation guide](https://docs.djangoproject.com/en/4.1/topics/http/middleware/)

7.Raw queries:[raw queries](https://docs.djangoproject.com/en/4.1/topics/db/sql/#:~:text=Django%20gives%20you%20two%20ways,ORM%20before%20using%20raw%20SQL!)
 writing the SQL queries to work with the models using raw method and also using The object django.db.connection 
from django

8.Rabbit MQ: RabbitMQ is a messaging broker - an intermediary for messaging.[guide](https://www.rabbitmq.com/tutorials/tutorial-one-python.html) 





```bash
important commands to implement the project:
1. python -m venv venv
2.source venv/Scripts/activate
3. pip install Django
4. django-admin startproject <project_name> .
5.python manage.py startapp <app_name>
```

## Features

```
User Login Registration and account verification from email
CRUD operation with Notes
Create and updating with labels
Running Tests
```
