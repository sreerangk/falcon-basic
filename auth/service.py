from sqlalchemy import select, insert
from db.engine import engine
from db.models import users
from utils.password import hash_password, verify_password

def create_user(email, password):
    with engine.begin() as conn:
        conn.execute(
            insert(users).values(
                email=email,
                password=hash_password(password)
            )
        )

def authenticate_user(email, password):
    with engine.connect() as conn:
        result = conn.execute(
            select(users).where(users.c.email == email)
        ).fetchone()

    if not result:
        return None

    if not verify_password(password, result.password):
        return None

    return result.id
