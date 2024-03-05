import ipdata

from celery import Celery
from celery.utils.log import get_task_logger



from app.models.ip_address import IpAddress
from app.models.user import User
from app.services.task import create_ip_address

celery = Celery('tasks', broker='amqp://rabbit:rabbit@127.0.0.1:5672//')

celery_log = get_task_logger(__name__)


@celery.task(name="create_task")
def create_ip_address_task(current_user, ip_address):
    if current_user and User.filter(User.username == current_user).first():
        current_user_id = User.filter(User.username == current_user).first().id

        ipdata.api_key = "cfbafad3637ca72504cfc36fe90b815bd23b5a400051a2054d765dd2"
        ipdata.endpoint = "https://eu-api.ipdata.co"
        
        response = ipdata.lookup(ip_address)

        return create_ip_address(response, current_user_id)
    else:
        return None
