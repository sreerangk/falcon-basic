import falcon
from auth.jwt import decode_token

# class AuthMiddleware:
#     def process_request(self, req, resp):
#         if req.path.startswith("/auth"):
#             return

#         auth_header = req.get_header("Authorization")
        
#         if not auth_header:
#             raise falcon.HTTPUnauthorized()

#         try:
#             token = auth_header.replace("Bearer ", "")
#             payload = decode_token(token)
#             req.context.user_id = payload["sub"]
#         except Exception:
#             raise falcon.HTTPUnauthorized()
        
class AuthMiddleware:
    def process_request(self, req, resp):
        if req.path.startswith("/auth"):
            return

        auth_header = req.get_header("Authorization")
        if not auth_header:
            raise falcon.HTTPUnauthorized(description="Missing Authorization header")

        try:
            token = auth_header.removeprefix("Bearer ").strip()
            payload = decode_token(token)
            req.context.user_id = payload["sub"]
        except Exception:
            raise falcon.HTTPUnauthorized(description="Invalid or expired token")


