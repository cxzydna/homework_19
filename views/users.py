from flask import request
from flask_restx import Resource, Namespace

from models import User, UserSchema
from setup_db import db
from utils import get_hash

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    @staticmethod
    def get():
        user_id = request.args.get('user_id')
        username = request.args.get('username')
        t = db.session.query(User)
        if user_id is not None:
            t = t.filter(User.id == user_id)
        if username is not None:
            t = t.filter(User.username == username)
        all_users = t.all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200

    @staticmethod
    def post():
        req_json = request.json
        ent = User(**req_json)
        ent.password = get_hash(req_json['password'])
        db.session.add(ent)
        db.session.commit()
        return "", 201, {"location": f"users/{ent.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @staticmethod
    def get(uid):
        user = db.session.query(User).get(uid)
        return UserSchema.dump(user), 200

    @staticmethod
    def put(uid):
        user = db.session.query(User).get(uid)
        req_json = request.json
        user.username = req_json.get('username')
        db.session.add(user)
        db.session.commit()
        return "", 204

    @staticmethod
    def delete(uid):
        user = db.session.query(User).get(uid)

        db.session.delete(user)
        db.session.commit()
        return "", 204
