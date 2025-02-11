from enum import IntEnum
from peewee import CharField, DateField, Model, SmallIntegerField

from app.models.db import db


class TodoStatus(IntEnum):
    todo = 0
    doing = 1
    done = 2


class TodoStatusField(SmallIntegerField):
    def db_value(self, value):
        if not isinstance(value, TodoStatus):
            raise TypeError("Wrong type, must be enum")
        return super().adapt(value.value)

    def python_value(self, value):
        return TodoStatus(value)


class Todo(Model):
    description = CharField()
    status = TodoStatusField()
    date_added = DateField()
    date_completed = DateField(null=True)

    class Meta:
        database = db
