from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core import database

from app.models import user, ip_address


app = FastAPI()

# Middleware
# https://fastapi.tiangolo.com/tutorial/middleware/

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection

database.db.connect()

# Create tables
database.db.create_tables([
    ip_address.IpAddress, 
    user.User
])

database.db.close()
