import json
from com.demimojo.netflix.model.movie import Movie
from flask import Flask, render_template, jsonify, Response
from flask_restful import marshal, fields

__author__ = 'mojosaurus'

app = Flask(__name__)

movie_suggestions_fields = {
    'text': fields.String
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/v1.0/movies/suggest/<string:chunk>', methods=['GET', 'POST'])
def suggest_movie(chunk):
    suggestions = Movie().suggest(chunk)
    return Response(json.dumps([x['text'] for x in map(lambda t: marshal(t, movie_suggestions_fields), suggestions['suggestions'][0]['options'])]), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=int('8080'))