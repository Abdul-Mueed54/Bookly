from celery import Celery
from src.mail import create_message, mail
from asgiref.sync import async_to_sync
from src.config import Config

c_app = Celery("Bookly", broker=Config.REDIS_URL, backend=Config.REDIS_URL)

# c_app.config_from_object('src.config')


@c_app.task()
def send_email(recipients: list[str], subject: str, body: str):
    message = create_message(recipients=recipients, subject=subject, body=body)

    async_to_sync(mail.send_message)(message)
