DEBUG = True
PLUGINS = [
    "fastack_sqlmodel",
    "fastack_migrate",
]

COMMANDS = []

DB_USER = "fastack_user"
DB_PASSWORD = "fastack_password"
DB_HOST = "localhost"
DB_PORT = 5888
DB_NAME = "celery_db"
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
# SQLALCHEMY_OPTIONS = {"echo": True}

# celery configuration
class Celery:
    broker_url = "amqp://strong_user:strong_password@localhost:5672/celery_vhost"
    result_backend = "redis://localhost:6900/0"
