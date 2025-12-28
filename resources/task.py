import falcon
from sqlalchemy import insert, select
from db.engine import engine
from db.models import tasks

class TaskResource:
    def on_get(self, req, resp):
        user_id = req.context.user_id

        with engine.connect() as conn:
            result = conn.execute(
                select(tasks).where(tasks.c.user_id == user_id)
            ).fetchall()
            print("TASKS FETCHED:", result)

        resp.media = [dict(row) for row in result]
        resp.media = [dict(row._mapping) for row in result]


    def on_post(self, req, resp):
        print("AUTH HEADER:", req.get_header("Authorization"))

        user_id = req.context.user_id
        data = req.media

        with engine.begin() as conn:
            conn.execute(
                insert(tasks).values(
                    title=data["title"],
                    user_id=user_id
                )
            )

        resp.status = falcon.HTTP_201
