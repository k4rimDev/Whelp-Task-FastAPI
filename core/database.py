import os
import peewee

from contextvars import ContextVar

from core.config import settings


db_state_default = {
    "closed": None, "conn": None,
    "ctx": None, "transactions": None
}

db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


if settings.DEBUG:
    db = peewee.MySQLDatabase('test_db', user='root',
                          password='test123',
                          host='db', port=3306)

else:
    db = peewee.MySQLDatabase(
        database = str(os.getenv('MYSQL_DATABASE')),
        user = str(os.getenv('MYSQL_USER')),
        password = str(os.getenv('MYSQL_ROOT_PASSWORD')),
        host = "db",
        port = 3306,
    )
