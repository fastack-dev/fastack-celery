from app import models, settings  # noqa
from app.controllers import init_controllers
from app.tasks import say_hello  # noqa
from celery import Celery  # noqa
from fastack import create_app

from fastack_celery import make_celery

app = create_app(settings)
init_controllers(app)

celery = make_celery(app)

# FIXME: I don't know why, when I uncomment the code below
# the task can't be called by .apply_async() (maybe blocked by another process?)

# @celery.on_after_configure.connect
# def init_jobs(sender: Celery, **kwds):
#     print("init jobs")
#     sig = say_hello.s()
#     sender.add_periodic_task(5, sig, task_id="say_hello_periodic_task")
