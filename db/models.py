from sqlalchemy import (
    Table, Column, Integer, String, MetaData, ForeignKey
)

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
)

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"))
)
