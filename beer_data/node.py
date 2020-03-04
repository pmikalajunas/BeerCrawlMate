from .util import haversine
from .models import Brewery

# Latitude and Longitude floating point precision.
COORDINATE_FLOATING_PRECISION = 6
# Max distance that helicopter can travel.
MAX_DISTANCE = 2000
# Id of a home (starting) node.
HOME_NODE_ID = -2
# First node in the matrix is the home node.
HOME_NODE_INDEX_MATRIX = 0


# Node is an entity in a distance matrix.
class Node(object):
    # matrix_id - node's index in the matrix.
    def __init__(self, matrix_id, id, name, lat, long, beer_count=0):
        self.matrix_id = matrix_id
        self.id = id
        self.name = name
        self.lat = round(lat, COORDINATE_FLOATING_PRECISION)
        self.long = round(long, COORDINATE_FLOATING_PRECISION)
        self.visited = False
        self.distance = 0
        self.beer_count = beer_count

    # Finds all the nodes within (MAX_DISTANCE / 2) radius.
    # Adds starting node at index HOME_NODE_INDEX_MATRIX.
    # Returns a list of nodes.
    def create_nodes(home_lat, home_long):
        # Start from home node, increment each time.
        node_index = HOME_NODE_INDEX_MATRIX
        # Initialize home node.
        nodes = [Node(node_index, HOME_NODE_ID, "Starting location", home_lat, home_long)]
        nodes[HOME_NODE_INDEX_MATRIX].visited = True

        for brewery in Brewery.objects.all():
            distance = haversine(home_lat, home_long, brewery.latitude, brewery.longitude)
            # If distance is more than it will take us to go back and forth, we'll ignore the brewery.
            if distance > (MAX_DISTANCE / 2):
                continue
            node_index += 1
            nodes.append(Node(
                node_index, brewery.id, brewery.name, brewery.latitude, brewery.longitude, brewery.beer_count
            ))
        return nodes

    # Made for debugging purposes to reflect Node's content.
    def __str__(self):
        return ("matrix_id: %d id: %d name: %s lat: %f long: %f" %
                (self.matrix_id, self.id, self.name, self.lat, self.long))
