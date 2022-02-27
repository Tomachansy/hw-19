from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from helpers.decorators import auth_required, admin_required
from implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        if rs:
            return res, 200
        else:
            return "", 404

    @admin_required
    def post(self):
        req_json = request.json
        genre = genre_service.create(req_json)

        return "", 201, {"location": f"/genres/{genre.id}"}


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        if r:
            return sm_d, 200
        else:
            return "", 404

    @admin_required
    def put(self, rid):
        if rid:
            req_json = request.json
            req_json["id"] = rid
            genre_service.update(req_json)
            return "", 204
        else:
            return "", 404

    @admin_required
    def patch(self, rid):
        if rid:
            req_json = request.json
            req_json["id"] = rid
            genre_service.update(req_json)
            return "", 204
        else:
            return "", 404

    @admin_required
    def delete(self, rid):
        if rid:
            genre_service.delete(rid)
            return "", 204
        else:
            return "", 404
