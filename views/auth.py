from flask import request, abort
from flask_restx import Resource, Namespace

from models import User
from setup_db import db
from utils import check_password, generate_token, check_token

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    @staticmethod
    def post():
        req_json = request.json
        data = db.session.query(User).filter(
            User.username == req_json['username']
        ).first()
        if data is None or not check_password(data.password, req_json['password']):
            abort(401)
        return generate_token(req_json)

    @staticmethod
    def put():
        print('lox')
        refresh_token = request.json["refresh_token"]
        data = check_token(refresh_token)
        print(data)
        if data:
            return generate_token(data), 204, {"location": "123"}
        else:
            abort(401)
