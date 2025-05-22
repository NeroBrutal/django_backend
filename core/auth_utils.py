import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY


def generate_tokens(user_id):
    access_payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=7),
    }
    refresh_payload = { 
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=7),
    }

    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm="HS256")
    return access_token, refresh_token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
