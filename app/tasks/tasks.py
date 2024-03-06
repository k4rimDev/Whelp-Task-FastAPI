import os
import ipdata

from celery import Celery
from celery.utils.log import get_task_logger

from app.models.user import User
from app.services.task import create_ip_address

from core.config import settings


if settings.DEBUG:
    celery = Celery('tasks', broker='amqp://rabbit:rabbit@127.0.0.1:5672//')
else:
    celery = Celery('tasks', 
                    broker='amqp://{user}:{password}@{host}:{port}//'.format(
                        user=os.getenv("RABBITMQ_DEFAULT_USER"),
                        password=os.getenv("RABBITMQ_DEFAULT_PASSWORD"),
                        host=os.getenv("RABBITMQ_DEFAULT_HOST"),
                        port=os.getenv("RABBITMQ_DEFAULT_PORT")
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
