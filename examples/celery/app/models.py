from enum import Enum
from typing import Optional

from fastack_sqlmodel import models
from sqlmodel import Field


class Counter(models.Model, table=True):
    class State(str, Enum):
        NOT_IN_QUEUE = "NOT IN QUEUE"
        IN_QUEUE = "IN QUEUE"
        TERMINATED = "TERMINATED"

    title: str = Field(max_length=255, nullable=False)
    counter: Optional[int] = Field(default=0, nullable=True)
    task_id: Optional[str]
    state: Optional[State] = State.NOT_IN_QUEUE

    def serialize(self) -> dict:
        data = super().serialize()
        data["title"] = self.title
        data["counter"] = self.counter
        data["task_id"] = self.task_id
        data["state"] = self.state
        return data
