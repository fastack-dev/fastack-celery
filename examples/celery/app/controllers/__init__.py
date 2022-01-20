from app.controllers.counter import CounterController
from fastack import Fastack


def init_controllers(app: Fastack):
    app.include_controller(CounterController())
