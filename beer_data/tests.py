from django.test import TestCase

from .solution import *
from .util import *
from .data_processor import MAX_DISTANCE

# Number by which we increase coordinate with each iteration.
CORD_INCREASE = 0.5


class SolutionTestCase(TestCase):

    # Unit test for retrieve_solution method.
    # Tries to form a solution with every possible lat and long.
    # Checks if travelled distance doesn't exceed MAX_DISTANCE.
    def test_retrieve_solution(self):
        lat = LAT_MIN
        long = LONG_MIN
        
        while lat != LAT_MAX:
            while long != LONG_MAX:                
                solution = Solution.retrieve_solution(lat, long)
                print('(TEST) lat: %f long: %f distance: %d' % (lat, long, solution.distance_travelled)) 
                self.assertTrue(solution.distance_travelled <= MAX_DISTANCE)
                long += CORD_INCREASE
            lat += CORD_INCREASE
            # Reset longitude
            long = LONG_MIN 
