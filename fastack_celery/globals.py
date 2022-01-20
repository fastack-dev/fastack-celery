from celery import Celery, Task, current_app, current_task

celery: Celery = current_app
celery_task: Task = current_task
