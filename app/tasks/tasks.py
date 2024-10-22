import os
import ipdata

from celery import Celery
from celery.utils.log import get_task_logger

from app.models.user import User
from app.services.task import create_ip_address

from core.config import settings


if settings.DEBUG:
    celery = Celery('tasks', broker='amqp://rabbit:rabbit@localhost:5672//')
else:
    celery = Celery('tasks', 
                    broker='amqp://{user}:{password}@rabbitmq:5672//'.format(
                        user=os.getenv("RABBITMQ_DEFAULT_USER"),
                        password=os.getenv("RABBITMQ_DEFAULT_PASS"),
                    ))    

celery_log = get_task_logger(__name__)


@celery.task(name="create_task")
def create_ip_address_task(current_user, ip_address):
    if current_user and User.filter(User.username == current_user).first():
        current_user_id = User.filter(User.username == current_user).first().id

        ipdata.api_key = settings.IPDATA_API_KEY
        ipdata.endpoint = "https://eu-api.ipdata.co"
        
        response = ipdata.lookup(ip_address)

        return create_ip_address(response, current_user_id)
    else:
        return None
