from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace("users")


@user_ns.route("/")
class UsersView(Resource):
    def get(self):
        users = user_service.get_all()
        if users:
            response = UserSchema(many=True).dump(users)
            return response, 200
        else:
            return "", 404

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)

        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route("/<int:uid>")
class UserView(Resource):
    def get(self, uid):
        u = user_service.get_one(uid)
        if u:
            sm_d = UserSchema().dump(u)
            return sm_d, 200
        else:
            return "", 404

    def put(self, uid):
        if uid:
            req_json = request.json
            req_json["id"] = uid
            user_service.update(req_json)
            return "", 204
        else:
            return "", 404

    def delete(self, uid):
        if uid:
            user_service.delete(uid)
            return "", 204
        else:
            return "", 404



