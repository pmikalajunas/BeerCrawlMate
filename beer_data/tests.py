from django.test import TestCase

from .solution import *
from .util import *
from .nearest_neighbour import MAX_DISTANCE
from .csv_reader import read_csv_data

# Number by which we increase coordinate with each iteration.
CORD_INCREASE = 4


# Tests algorithm with every possible lat and long.
# Checks if travelled distance doesn't exceed MAX_DISTANCE.
def test_algorithm(test, algorithm):
    lat = LAT_MIN
    long = LONG_MIN

    while lat <= LAT_MAX:
        while long <= LONG_MAX:
            solution = retrieve_solution(lat, long, algorithm)
            test.assertTrue(solution.distance_travelled <= MAX_DISTANCE)
            long += CORD_INCREASE
        lat += CORD_INCREASE
        # Reset longitude
        long = LONG_MIN


class NearestNeighbourTest(TestCase):

    def setUp(self):
        # Reads beer data from supplied csv files, initializes DB.
        read_csv_data()

    def test_nearest_neighbour(self):
        test_algorithm(self, 'Nearest Neighbour')


class SimulatedAnnealingTest(TestCase):

    def setUp(self):
        # Reads beer data from supplied csv files, initializes DB.
        read_csv_data()

    def test_simulated_annealing(self):
        test_algorithm(self, 'Simulated Annealing')


class ChristofidesTest(TestCase):

    def setUp(self):
        # Reads beer data from supplied csv files, initializes DB.
        read_csv_data()

    def test_christofides(self):
        test_algorithm(self, 'Christofides')



