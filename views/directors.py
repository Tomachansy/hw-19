from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from helpers.decorators import auth_required, admin_required
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        if rs:
            return res, 200
        else:
            return "", 404

    @admin_required
    def post(self):
        req_json = request.json
        director = director_service.create(req_json)

        return "", 201, {"location": f"/directors/{director.id}"}


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        if r:
            return sm_d, 200
        else:
            return "", 404

    @admin_required
    def put(self, rid):
        if rid:
            req_json = request.json
            req_json["id"] = rid
            director_service.update(req_json)
            return "", 204
        else:
            return "", 404

    @admin_required
    def patch(self, rid):
        if rid:
            req_json = request.json
            req_json["id"] = rid
            director_service.update_partial(req_json)
            return "", 204
        else:
            return "", 404

    @admin_required
    def delete(self, rid):
        if rid:
            director_service.delete(rid)
            return "", 204
        else:
            return "", 404
