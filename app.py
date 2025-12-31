import falcon
from middleware.auth import AuthMiddleware
from auth.routes import RegisterResource, LoginResource
from resources.task import TaskResource
import logging

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = falcon.App(middleware=[AuthMiddleware()])

app.add_route("/auth/register", RegisterResource())
app.add_route("/auth/login", LoginResource())
app.add_route("/tasks", TaskResource())


from waitress import serve

if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=8000)



