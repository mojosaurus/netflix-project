from com.demimojo import constant
import os

__author__ = 'mojosaurus'

"""
The files in this package help load data into elasticsearch
"""

class _Constants:
    @constant
    def DATA_DIR():
        return "%s/%s" % (os.path.dirname(os.path.abspath(__file__)), "../../../../raw-data/")

    @constant
    def MOVIE_TITLES():
        return "%s%s" % (_Constants().DATA_DIR, 'movie_titles.txt')

    @constant
    def LOG_DIR():
        return "%s/%s/%s" % (os.path.dirname(os.path.abspath(__file__)), "../../../../raw-data", 'log')


Constants = _Constants()

