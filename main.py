from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import database


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
database.db.close()
