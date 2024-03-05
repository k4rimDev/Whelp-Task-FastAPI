from peewee import Model

from core.database import db


class BaseModel(Model):
    class Meta:
        database = db
