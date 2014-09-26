from com.demimojo import constant

__author__ = 'mojosaurus'


class _ElasticSearchSettings:
    @constant
    def netflix_index():
        return 'netflix'


    @constant
    def movie_index_settings():
        return {
            'settings': {
                'analysis': {
                    'filter': {
                        'autocomplete_filter': {
                            'type': 'edge_ngram',
                            'min_gram': 1,
                            'max_gram': 20
                        }
                    },
                    'analyzer': {
                        'autocomplete': {
                            'type': 'custom',
                            'tokenizer': 'standard',
                            'filter': [
                                'lowercase',
                                'autocomplete_filter'
                            ]
                        }
                    }
                }
            }
        }

    @constant
    def movie_mapping_type():
        return {
            'movie': {
                'properties': {
                    'id': {
                        'type': 'integer'
                    },
                    'year': {
                        'type': 'date'
                    },
                    'name': {
                        'type': 'string',
                    },
                    'num_ratings' : {
                        'type': 'integer'
                    },
                    'avg_rating': {
                        'type': 'double'
                    },
                    'suggest': {
                        'type': 'completion',
                        'index_analyzer': 'simple',
                        'search_analyzer': 'simple',
                        'payloads': 'true'

                    }
                }
            }
        }

    @constant
    def user_mapping_type():
        return {
            'user': {
                'properties': {
                    'id': {
                        'type': 'integer'
                    },
                    'num_ratings': {
                        'type': 'integer'
                    },
                    'avg_rating': {
                        'type': 'double'
                    }
                }
            }
        }

    @constant
    def rating_mapping_type():
        return {
            'rating': {
                'properties': {
                    'movie_id': {
                        'type': 'integer'
                    },
                    'user_id': {
                        'type': 'integer'
                    },
                    'rating': {
                        'type': 'double'
                    },
                    'normalized_rating': {
                        'type': 'double'
                    }
                }
            }
        }

    @constant
    def movie_suggest():
        return {
            "suggestions" : {
                "text" : "india",
                "completion" : {
                  "field" : "suggest"
                }
              }
            }

ElasticSearchSettings = _ElasticSearchSettings()