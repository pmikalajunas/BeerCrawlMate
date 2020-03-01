
# Latitude and Longitude floating point precision.
COORDINATE_FLOATING_PRECISION = 6

# Node is an entity in a distance matrix.
class Node:
    # matrix_id - node's index in the matrix.
    def __init__(self, matrix_id, id, name, lat, long):
        self.matrix_id = matrix_id
        self.id = id
        self.name = name
        self.lat = round(lat, COORDINATE_FLOATING_PRECISION)
        self.long = round(long, COORDINATE_FLOATING_PRECISION)
        self.visited = False
        self.distance = 0

    # Made for debugging purposes to reflect Node's content.
    def __str__(self):
        return ("matrix_id: %d id: %d name: %s lat: %f long: %f" % 
                (self.matrix_id, self.id, self.name, self.lat, self.long))