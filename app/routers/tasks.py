import socket

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi_jwt_auth2 import AuthJWT

from app.services.task import get_status_of_task

from app.tasks.tasks import create_ip_address_task


router = APIRouter()


@router.post("/task-your-ip", description="""
    Create a task in MySQL, send it to celery, and return task ID
    Input will be IP address of registered User.

    Create a free account on https://ipdata.co/
    Fetch data from https://ipdata.co/ regarding provided IP and save details into DB
    """)
def task_your_ip(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        ip_address = socket.gethostbyname(socket.gethostname())
        task = create_ip_address_task.delay(current_user, ip_address)
        return {"task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Task failed to create")
    

@router.post("/task-specific-ip", description="""
    Create a task in MySQL, send it to celery, and return task ID
    Input will be IP address of registered User.

    Create a free account on https://ipdata.co/
    Fetch data from https://ipdata.co/ regarding provided IP and save details into DB
    """)
def task_specific_ip(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        task = create_ip_address_task.delay(current_user, '51.253.30.82')
        return {"task_id": task.id} 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Task failed to create")


@router.get("/status/{id}", description="Show the result of the task")
def status(id: int, Authorize: AuthJWT = Depends()):
    return get_status_of_task(id)
    