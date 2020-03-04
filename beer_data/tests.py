from django.test import TestCase

from .solution import *
from .util import *
from .nearest_neighbour import MAX_DISTANCE
from .csv_reader import read_csv_data

# Number by which we increase coordinate with each iteration.
CORD_INCREASE = 4


class SolutionTestCase(TestCase):

    def setUp(self):
        # Reads beer data from supplied csv files, initializes DB.
        read_csv_data()

    # Unit test for retrieve_solution method.
    # Tries to form a solution with every possible lat and long.
    # Checks if travelled distance doesn't exceed MAX_DISTANCE.
    def test_retrieve_solution(self):
        lat = LAT_MIN
        long = LONG_MIN
        
        while lat <= LAT_MAX:
            while long <= LONG_MAX:                
                solution = Solution.retrieve_solution(lat, long, 'Nearest Neighbour')
                # Print ones that travelled somewhere.
                if solution.distance_travelled > 0:
                    print('(TEST) lat: %f long: %f distance: %d beer count: %d' 
                        % (lat, long, solution.distance_travelled, solution.beer_count))                 
                self.assertTrue(solution.distance_travelled <= MAX_DISTANCE)
                long += CORD_INCREASE
            lat += CORD_INCREASE
            # Reset longitude
            long = LONG_MIN 



