import random

from app.models import Counter
from celery import shared_task
from fastack_sqlmodel.globals import db

from fastack_celery.globals import celery


@shared_task
def say_hello():
    msg = random.choice(["World", "Mars", "Ghozali! dirjen pajak disini"])
    print("Hello " + msg)


@shared_task
def counter_task(id: int):
    session = db.open()
    with session.begin():
        obj: Counter = session.query(Counter).where(Counter.id == id).first()
        if obj:
            print(f"start counting #{id}")
            obj.counter += 1
            state = obj.state
            if state is None or state == Counter.State.NOT_IN_QUEUE:
                obj.state = Counter.State.NOT_IN_QUEUE
            elif state == Counter.State.TERMINATED:
                task_id = obj.task_id  # or current_task.request.id
                celery.control.revoke(task_id, terminate=True)
                obj.task_id = None
            else:
                obj.state = Counter.State.IN_QUEUE
                counter_task.apply_async(args=(id,), countdown=1, task_id=obj.task_id)

            obj.save(session)

        else:
            print(f"Object with id #{id} not found")
