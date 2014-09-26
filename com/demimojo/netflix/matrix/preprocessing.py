__author__ = 'mojosaurus'


import sys
from com.demimojo.netflix.loader import Constants
from sklearn.preprocessing import normalize
import csv
from com import logger
import glob
from scipy.sparse import lil_matrix
import numpy as np

class PreProcess():
    def __init__(self):
        logger.info("Starting pre-procesing")

    def process(self):
        self.__initDataStructures()
        self.__constructUberMatrix()
        self.__normalizeMatrix()

    def getNormalizedMatrix(self):
        return self.normalizedMatrix

    def getRating(self, row, col):
        return self.uberMatrix[row, col]

    def getNormalizedRating(self, row, col):
        return self.normalizedMatrix[row, col]

    def getAverageUserRating(self, userId):
        return self.userAvg[userId]

    def getAverageMovieRating(self, movieId):
        return self.movieAvg[movieId]

    def getNumUserRating(self, userId):
        return self.userCnt[userId]

    def getNumMovieRating(self, movieId):
        logger.info("Getting rating count got movie %d " % movieId)
        return self.movieCnt[movieId]

    def __initDataStructures(self):
        logger.info("Initialising the sparse matrices - uber and normalized")
        self.uberMatrix = lil_matrix((2649430, 17770), dtype=np.float64)
        self.normalizedMatrix = lil_matrix((2649430, 17770), dtype=np.float64)

        logger.info("Initialising associated arrays")
        self.userAvg = [0 for i in range(0, 2649430)]
        self.userCnt = [0 for i in range(0, 2649430)]
        self.movieAvg = [0 for i in range(0, 17771)]
        self.movieCnt = [0 for i in range(0, 17771)]
        logger.info("Arrays initialized")


    def __constructUberMatrix(self):
        logger.info("Constructing the uber matrix")
        files = sorted(glob.glob(Constants.DATA_DIR + "training_set/*.txt"))
        for file in files:
            with open(file, 'r') as f:
                elements = [line.split(',', 2) for line in f]
                for element in elements:
                    if len(element) == 1:
                        movieId = int(element[0].replace(':', '').rstrip())
                        logger.info("Starting movie %d " % movieId)
                    else:
                        userId = int(element[0])
                        rating = float(element[1])
                        self.uberMatrix[userId, movieId] = float(rating)

                        # Now, calculate the average for the movie and the user.
                        self.userAvg[userId] = (self.userAvg[userId] + rating) / 2 if self.userAvg[userId] != 0 else rating
                        self.userCnt[userId] += 1
                        self.movieAvg[movieId] = (self.movieAvg[movieId] + rating) / 2 if self.movieAvg[movieId] != 0 else rating
                        self.movieCnt[movieId] += 1
                logger.info("Movie id %d ended " % movieId)
                f.close()
        logger.info("Uber matrix constructed")

    def __writerFiles(self):
        logger.info("Writing file user_average.csv")
        with open(Constants.DATA_DIR+'user_average.csv', 'w') as fh:
            writer = csv.writer(fh, delimiter=',')
            for i in range(1, len(self.userAvg)):
                writer.writerow([i, self.userCnt[i], self.userAvg[i]])
            fh.close()

        logger.info("Writing file movie_average.csv")
        with open(Constants.DATA_DIR+'movie_average.csv', 'w') as fh:
            writer = csv.writer(fh, delimiter=',')
            for i in range(1, len(self.movieAvg)):
                writer.writerow([i, self.movieCnt[i], self.movieAvg[i]])
            fh.close()


    def __normalizeMatrix(self):
        # Now, onto normalising the matrix.
        logger.info("Intializing the normalized matrix")

        rows, cols = self.uberMatrix.nonzero()
        for i in range(0, len(rows)):
            row = rows[i]
            col = cols[i]
            val = self.uberMatrix[row, col]
            normalizedValue = self.userAvg[row] - val
            self.normalizedMatrix[row, col] = normalizedValue

        # Delete the object to free up memory. We will need it soon.
        logger.info("Matrix normalized")
#
# process = PreProcess()
# process.process()
#
# print process.getNormalizedScore(2643247, 30)