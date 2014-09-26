from com.demimojo.netflix.resources import movies
from flask_restful.utils import cors

__author__ = 'mojosaurus'

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.views import MethodView
from flask_restful import Api, Resource, reqparse, marshal

app = Flask(__name__, static_url_path = "")
api = Api()
app.config.from_object('config.DebugConfiguration') #load our local config file

api.add_resource(movies.MovieSuggestAPI, '/v1.0/movies/suggest/<string:chunk>')
api.decorators=[cors.crossdomain(origin='*', headers=['accept', 'Content-Type'])]

if __name__ == '__main__':
    app.run(debug = True)