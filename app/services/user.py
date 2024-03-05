from fastapi import HTTPException

from app.models.user import User
from core.hashing import Hash
from app.schemas.user import BaseUser


def create_user(request: BaseUser):
    username = request.username
    password = request.password
    email = request.email
    
    if not (username and password and email):
        raise HTTPException(status_code=400, detail="Username, password, and email are required")

    existing_user = User.filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = Hash.bcrypt(password)
    
    user = User(username=username, password=hashed_password, email=email)
    user.save()
    
    return user
