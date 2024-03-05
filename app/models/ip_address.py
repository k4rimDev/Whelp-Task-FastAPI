from peewee import CharField, IntegerField, BooleanField, ForeignKeyField

from app.models.base import BaseModel
from app.models.user import User


class IpAddress(BaseModel):
    ip = CharField(20)
    user = ForeignKeyField(User, backref='ips', null=True)
    is_eu = BooleanField(default=False)
    city = CharField(120, null=True)
    region = CharField(120, null=True)
    region_code = CharField(120, null=True)
    country_name = CharField(120, null=True)
    country_code = CharField(120, null=True)
    continent_name = CharField(120, null=True)
    continent_code = CharField(120, null=True)
    latitude = CharField(120, null=True)
    longitude = CharField(120, null=True)
    postal = CharField(120, null=True)
    calling_code = CharField(120, null=True)
    flag = CharField(120, null=True, column_name='emoji_flag')
