import falcon
from auth.service import create_user, authenticate_user
from auth.jwt import create_token

class RegisterResource:
    def on_post(self, req, resp):
        data = req.media
        create_user(data["email"], data["password"])
        resp.status = falcon.HTTP_201

class LoginResource:
    def on_post(self, req, resp):
        data = req.media
        user_id = authenticate_user(data["email"], data["password"])

        if not user_id:
            raise falcon.HTTPUnauthorized()

        token = create_token(user_id)
        resp.media = {"token": token}
