import jwt
from datetime import datetime, timedelta
from config.settings import SECRET_KEY

def create_token(user_id):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    payload["sub"] = int(payload["sub"])
    return payload


