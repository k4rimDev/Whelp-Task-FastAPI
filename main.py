from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from app.models import user, ip_address
from app.routers.main import api_router

from core import database


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    swagger_ui_parameters={"syntaxHighlight": True}
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

# Database connection
database.db.connect()

# Create tables
database.db.create_tables([
    ip_address.IpAddress, 
    user.User
])

database.db.close()
