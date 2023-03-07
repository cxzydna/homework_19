import jwt
from flask import request, abort

from constants import SECRET_HERE, ALGO
from utils import check_token


def auth_required(func):
    def wrapper(*args, **kwargs):
        access_token = request.json['access_token']
        if check_token(access_token):
            return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, SECRET_HERE, algorithms=[ALGO])
            role = user.get("role")
            if role != "admin":
                abort(400)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper
