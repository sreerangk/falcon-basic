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
        
# class AuthMiddleware:
#     def process_request(self, req, resp):
#         if req.path.startswith("/auth"):
#             return

#         auth_header = req.get_header("Authorization")
#         if not auth_header:
#             raise falcon.HTTPUnauthorized(description="Missing Authorization header")

#         try:
#             token = auth_header.removeprefix("Bearer ").strip()
#             payload = decode_token(token)
#             req.context.user_id = payload["sub"]
#         except Exception:
#             raise falcon.HTTPUnauthorized(description="Invalid or expired token")

import logging
from jwt import (
    ExpiredSignatureError,
    InvalidTokenError,
    DecodeError,
    InvalidSignatureError,
)

logger = logging.getLogger(__name__)

class AuthMiddleware:
    def process_request(self, req, resp):
        if req.path.startswith("/auth"):
            return

        auth_header = req.get_header("Authorization")
        if not auth_header:
            raise falcon.HTTPUnauthorized(
                title="Unauthorized",
                description="Authentication required"
            )

        if not auth_header.startswith("Bearer "):
            logger.warning("Invalid auth header format: %s", auth_header)
            raise falcon.HTTPUnauthorized(
                title="Unauthorized",
                description="Invalid authentication credentials"
            )

        token = auth_header[len("Bearer "):].strip()
        if not token:
            logger.warning("Empty bearer token")
            raise falcon.HTTPUnauthorized(
                title="Unauthorized",
                description="Invalid authentication credentials"
            )

        try:
            payload = decode_token(token)

            user_id = payload.get("sub")
            if not user_id:
                logger.warning("JWT missing sub claim: %s", payload)
                raise falcon.HTTPUnauthorized(
                    title="Unauthorized",
                    description="Invalid authentication credentials"
                )

            req.context.user_id = user_id

        except ExpiredSignatureError:
            logger.info("JWT expired")
            raise falcon.HTTPUnauthorized(
                title="Unauthorized",
                description="Invalid authentication credentials"
            )

        except (InvalidSignatureError, DecodeError, InvalidTokenError) as e:
            logger.warning("JWT decode failed: %s", str(e))
            raise falcon.HTTPUnauthorized(
                title="Unauthorized",
                description="Invalid authentication credentials"
            )

        except Exception as e:
            logger.exception("Unexpected auth error")
            raise falcon.HTTPInternalServerError(
                title="Internal Server Error",
                description="Authentication service failure"
            )