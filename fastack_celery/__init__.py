import asyncio

from asgi_lifespan import LifespanManager
from celery import Celery, Task
from fastack import Fastack
from fastack.context import _app_ctx_stack


def make_celery(app: Fastack, name: str = "main") -> Celery:
    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            async def executor():
                token = None
                try:
                    async with LifespanManager(app):
                        token = _app_ctx_stack.set(app)
                        return self.run(*args, **kwargs)
                finally:
                    if token:
                        _app_ctx_stack.reset(token)

            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()

            task = loop.create_task(executor())
            return loop.run_until_complete(task)

    celery = Celery(
        name,
        task_cls=ContextTask,
    )
    celery.set_default()
    celery_conf = getattr(app.state.settings, "Celery", object())
    celery.config_from_object(celery_conf)
    celery.autodiscover_tasks(["app"], force=True)
    return celery
