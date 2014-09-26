import time
from com import logger
from com.demimojo.netflix.elasticsearch.settings import ElasticSearchSettings
from com.demimojo.netflix.loader import Constants
from com.demimojo.netflix.matrix.preprocessing import PreProcess
from elasticsearch import Elasticsearch
from elasticsearch import helpers

__author__ = 'mojosaurus'


class MovieLoader:
    def __init__(self):
        self.es = Elasticsearch()
        self.process = PreProcess()
        self.process.process()
        self.setupElasticSearch()

    def setupElasticSearch(self):
        logger.info("Setting up elasticsearch for netflix database")
        logger.info("Deleting pre-existing indices")
        self.es.indices.delete(index=ElasticSearchSettings.netflix_index,  ignore=[404])

        logger.info("Creating netflix index")
        self.es.indices.create(index=ElasticSearchSettings.netflix_index)
        time.sleep(5)
        logger.info("Closing the index to update index settings")
        self.es.indices.close(index=ElasticSearchSettings.netflix_index)
        time.sleep(5)
        self.es.indices.put_settings(index=ElasticSearchSettings.netflix_index,
                                     body=ElasticSearchSettings.movie_index_settings)

        logger.info("Settings done. Opening up the index")
        self.es.indices.open(index=ElasticSearchSettings.netflix_index)
        time.sleep(5)

        logger.info("Creating mappings - movie")
        self.es.indices.put_mapping(index=ElasticSearchSettings.netflix_index,
                                    doc_type='movie',
                                    body=ElasticSearchSettings.movie_mapping_type
        )

        logger.info("Creating mappings - user")
        self.es.indices.put_mapping(index=ElasticSearchSettings.netflix_index,
                                    doc_type='user',
                                    body=ElasticSearchSettings.user_mapping_type
        )

        logger.info("Creating mappings - ratings")
        self.es.indices.put_mapping(index=ElasticSearchSettings.netflix_index,
                                    doc_type='rating',
                                    body=ElasticSearchSettings.rating_mapping_type
        )

    def indexMovies(self):
        movies = self.__getMovies()
        bulk_movies = [movies[i::100] for i in range(100)]
        for chunk in bulk_movies:
            actions = []
            for movie in chunk:
                name_chunks = movie[2].rstrip().split(' ')
                suggest_chunks = [name_chunks[i] for i in range(0, len(name_chunks))]
                suggest_chunks.extend([" ".join(name_chunks[0:i]) for i in range(0, len(name_chunks))])
                movieId = int(movie[0])
                action = {
                    '_index': 'netflix',
                    '_type': 'movie',
                    '_id': movieId,
                    'year': movie[1],
                    'name': movie[2].rstrip(),
                    'num_ratings': self.process.getNumMovieRating(movieId),
                    'avg_rating' : self.process.getAverageMovieRating(movieId),
                    'suggest': {'input': suggest_chunks,
                                'output': movie[2].rstrip(),
                    }
                }
                print action
                actions.append(action)
            ret = helpers.bulk(self.es, actions=actions)
            print ret

    def indexUsers(self):
        users = self.__getUsers()
        bulk_users = [users[i::100] for i in range(100)]
        for chunk in bulk_users:
            actions = []
            for user in chunk:
                action = {
                    '_index': 'netflix',
                    '_type': 'user',
                    '_id': user,
                    'num_ratings': self.process.getNumUserRating(user),
                    'avg_rating' : self.process.getAverageUserRating(user)
                }
                print action
                actions.append(action)
            ret = helpers.bulk(self.es, actions=actions)
            print ret


    def indexRatings(self):
        ratings = self._getRatings()
        bulk_ratings = [ratings[i::100] for i in range(100)]
        for chunk in bulk_ratings:
            actions = []
            for rating in chunk:
                action = {
                    '_index': 'netflix',
                    '_type': 'rating',
                    'user_id': int(rating[0]),
                    'movie_id': int(rating[1]),
                    'rating': float(rating[2]),
                    'normalized_rating': float(rating[3])

                }
                actions.append(action)
            ret = helpers.bulk(self.es, actions=actions)
            print ret

    def __getUsers(self):
        ret = [id for id in range(1,2649429)]
        return ret

    def __getMovies(self):
        with open(Constants.MOVIE_TITLES, 'r') as f:
            movies = [line.split(',', 2) for line in f]
            return movies

    def _getRatings(self):
        rows, cols = self.process.getNormalizedMatrix().nonzero()
        ratings = []
        for i in range(0, len(rows)):
            row = rows[i]
            col = cols[i]
            normalizedRating = self.process.getNormalizedRating(row, col)
            rating = self.process.getRating(row, col)
            ratings.append([row,col,rating, normalizedRating])

        return ratings


if __name__ == "__main__":
    movies = MovieLoader()
    movies.indexMovies()
    movies.indexUsers()
    movies.indexRatings()