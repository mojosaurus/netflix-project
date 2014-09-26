from com.demimojo.netflix.elasticsearch.settings import ElasticSearchSettings
from elasticsearch import Elasticsearch

__author__ = 'mojosaurus'

class Movie:
    def __init__(self):
        self.es = Elasticsearch()

    def suggest(self, chunk):
        suggest_txt = ElasticSearchSettings.movie_suggest
        suggest_txt['suggestions']['text'] = chunk
        ret = self.es.suggest(index=ElasticSearchSettings.movie_index,
                        body=suggest_txt
                        )
        return ret