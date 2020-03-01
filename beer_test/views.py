from django.shortcuts import render
from django.http import HttpResponse

from beer_data.csv_reader import *
from beer_data.data_processor import *
from beer_data.forms import SubmitForm

# Every solution will have 2 home nodes, as we have to get back home.
HOME_NODE_COUNT = 2

# 51.355468, 11.100790
def home_view(request):
    read_csv_data()

    # Path that we are going to take.
    solution = []
    beers = []
    beer_count = 0
    distance_travelled = 0
    brewery_count = 0
    time = 0
    home_lat = 54.8985
    home_long = 23.9036
    submit_form = SubmitForm()
    if request.method == 'POST':
        submit_form = SubmitForm(request.POST)
        if submit_form.is_valid():
            home_lat = submit_form.cleaned_data.get('lat')
            home_long = submit_form.cleaned_data.get('long')
            # Measure execution time.
            start = timeit.default_timer()
            nodes = create_nodes(home_lat, home_long)
            if len(nodes) > 1:
                matrix = construct_distance_matrix(nodes)
                print("Matrix contains %d nodes" % len(nodes))
                distance_travelled, solution = TSP(matrix, nodes)
                stop = timeit.default_timer()
                time = stop - start
                brewery_count = len(solution) - HOME_NODE_COUNT
                print("Total distance travelled: %f" % distance_travelled)
                beers = get_beers(solution)
                beer_count = len(beers)

            
    data = {
        "solution": solution,
        "form": submit_form,
        "distance_travelled": round(distance_travelled),
        "beers": beers,
        "beer_count": len(beers),
        "brewery_count": brewery_count,
        "home_lat": home_lat,
        "home_long": home_long,
        "running_time": 0
    }
    return render(request, 'home.html', data)