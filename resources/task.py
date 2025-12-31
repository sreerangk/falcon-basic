import falcon
from sqlalchemy import insert, select
from db.engine import engine
from db.models import tasks

# class TaskResource:
#     def on_get(self, req, resp):
#         user_id = req.context.user_id

#         with engine.connect() as conn:
#             result = conn.execute(
#                 select(tasks).where(tasks.c.user_id == user_id)
#             ).fetchall()

#         resp.media = [dict(row) for row in result]
#         resp.media = [dict(row._mapping) for row in result]


#     def on_post(self, req, resp):

#         user_id = req.context.user_id
#         data = req.media

#         with engine.begin() as conn:
#             conn.execute(
#                 insert(tasks).values(
#                     title=data["title"],
#                     user_id=user_id
#                 )
#             )

#         resp.status = falcon.HTTP_201
import logging
logger = logging.getLogger(__name__)

class TaskResource:
    def on_get(self, req, resp):
        user_id = req.context.user_id

        try:
            with engine.connect() as conn:
                result = conn.execute(
                    select(tasks).where(tasks.c.user_id == user_id)
                ).fetchall()

        except Exception:
            logger.exception("Failed to fetch tasks", extra={"user_id": user_id})
            raise falcon.HTTPInternalServerError(
                title="Internal Server Error",
                description="Could not fetch tasks"
            )

        resp.media = [dict(row._mapping) for row in result]
    
    def on_post(self, req, resp):
        user_id = req.context.user_id
        data = req.media

        title = data.get("title")
        if not title:
            raise falcon.HTTPBadRequest(
                title="Bad Request",
                description="title is required"
            )

        try:
            with engine.begin() as conn:
                result = conn.execute(
                    insert(tasks)
                    .values(title=title, user_id=user_id)
                    .returning(tasks.c.id)
                )
                task_id = result.scalar()

        except Exception:
            logger.exception("Failed to create task", extra={"user_id": user_id})
            raise falcon.HTTPInternalServerError(
                title="Internal Server Error",
                description="Could not create task"
            )

        resp.status = falcon.HTTP_201
        resp.media = {
            "id": task_id,
            "title": title
        }
