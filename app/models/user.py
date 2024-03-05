from datetime import datetime

from peewee import CharField, DateTimeField

from app.models.base import BaseModel


class User(BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    join_date = DateTimeField(default=datetime.now)
