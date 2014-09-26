from com.demimojo.netflix.model.movie import Movie

__author__ = 'mojosaurus'

from flask_restful import Api, Resource, fields, marshal
from flask_restful.utils import cors

movie_suggestions_fields = {
    'text': fields.String
}


class MovieSuggestAPI(Resource):
    def __init__(self):
        super(MovieSuggestAPI, self).__init__()
        self.movie = Movie()

    @cors.crossdomain(origin='*')
    def get(self, chunk):
        suggestions = self.movie.suggest(chunk=chunk)

        return {'suggestions': [x['text'] for x in map(lambda t: marshal(t, movie_suggestions_fields), suggestions['suggestions'][0]['options'])]}, 200, {'Access-Control-Allow-Origin': '*'}

