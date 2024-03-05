from datetime import timedelta

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi_jwt_auth2 import AuthJWT

from app.schemas.user import (
    ShowUser, BaseUser, 
    LoginUser
)

from app.services.user import create_user
from app.models.user import User

from core.hashing import Hash
from core.config import settings


router = APIRouter()

@AuthJWT.load_config
def get_config():
    return settings


@router.post("/register", response_model=ShowUser, description="Register a user")
def signup(request: BaseUser):
    return create_user(request)


@router.post('/login', description='JWT sign in')
def login(user: LoginUser, Authorize: AuthJWT = Depends()):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username or password not provided")

    my_user = User.filter(User.username == user.username).first()
    if not my_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not Hash.verify(my_user.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    expires = timedelta(days=1)
    access_token = Authorize.create_access_token(
        subject=user.username, expires_time=expires)
    refresh_token = Authorize.create_refresh_token(subject=user.username)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expire_at (with days)": expires.days
    }

@router.get('/user')
def user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        return {"user": current_user}
    except HTTPException:
        raise HTTPException(status_code=401, detail="Not authorized")


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        new_access_token = Authorize.create_access_token(subject=current_user)
        return {"access_token": new_access_token}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
