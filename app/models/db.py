`# from datetime import datetime
# from zoneinfo import ZoneInfo

# from sqlalchemy import event
from sqlmodel import Field, Relationship, SQLModel


class Base(SQLModel):
    __abstract__ = True
    __table_args__ = {"schema": "my_schema"}
