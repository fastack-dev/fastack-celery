from typing import List, Optional

from app.models import Counter
from app.tasks import counter_task
from fastack import ListController
from fastack.decorators import route
from fastack_sqlmodel.globals import db
from fastack_sqlmodel.session import Session
from fastapi import Query, Response
from pydantic import BaseModel
from sqlalchemy import desc

from fastack_celery.globals import celery


class CounterBody(BaseModel):
    title: str
    counter: Optional[int] = 0


class CounterController(ListController):
    def post(self, body: CounterBody):
        session: Session = db.open()
        with session:
            counter: Counter = Counter.create(session, **body.dict())
            print("Counter:", counter)
            result = counter_task.apply_async(args=(counter.id,), countdown=5)
            print("Task:", result)
            counter.task_id = result.task_id
            counter.state = Counter.State.IN_QUEUE
            counter.save(session)

        return self.json("Scheduled", counter)

    @route("/{id}")
    def get(self, id: int):
        session: Session = db.open()
        with session:
            counter: Counter = session.query(Counter).where(Counter.id == id).first()
            if not counter:
                return self.json("Not Found", status=404)
            return self.json("Task", counter)

    def put(self, id: int, state: Counter.State = Counter.State.NOT_IN_QUEUE):
        session: Session = db.open()
        with session.begin():
            counter: Counter = session.query(Counter).where(Counter.id == id).first()
            if not counter:
                return self.json("Not Found", status=404)

            counter.state = state
            task_id = counter.task_id
            if state == Counter.State.NOT_IN_QUEUE and task_id:
                counter.task_id = None
                celery.control.revoke(task_id, terminate=True)
            elif state == Counter.State.IN_QUEUE and not task_id:
                result = counter_task.apply_async(args=(id,))
                counter.task_id = result.task_id
            elif state == Counter.State.TERMINATED and task_id:
                celery.control.revoke(task_id, terminate=True)
                counter.task_id = None

            counter.save(session)
        return self.json("Updated", counter)

    def list(
        self, page: int = Query(1, gt=0), page_size: int = Query(10, gt=0)
    ) -> Response:
        session: Session = db.open()
        with session:
            data: List[Counter] = (
                session.query(Counter).order_by(desc(Counter.id)).all()
            )
            return self.get_paginated_response(data, page, page_size)
