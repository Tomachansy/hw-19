from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from helpers.decorators import auth_required, admin_required
from implemented import movie_service

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
        }
        all_movies = movie_service.get_all(filters)
        res = MovieSchema(many=True).dump(all_movies)
        if all_movies:
            return res, 200
        else:
            return "", 404

    @admin_required
    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    @auth_required
    def get(self, bid):
        b = movie_service.get_one(bid)
        if b:
            sm_d = MovieSchema().dump(b)
            return sm_d, 200
        else:
            return "", 404

    @admin_required
    def put(self, bid):
        if bid:
            req_json = request.json
            if "id" not in req_json:
                req_json["id"] = bid
            movie_service.update(req_json)
            return "", 204
        else:
            return "", 404

    @admin_required
    def patch(self, bid):
        if bid:
            req_json = request.json
            req_json["id"] = bid
            movie_service.update_partial(req_json)
            return "", 204
        else:
            return "", 404

    @admin_required
    def delete(self, bid):
        if bid:
            movie_service.delete(bid)
            return "", 204
        else:
            return "", 404
