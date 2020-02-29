from django.shortcuts import render
from django.http import HttpResponse

from beer_data.csv_reader import *
from beer_data.data_processor import *
from beer_data.forms import SubmitForm

# 51.355468, 11.100790
def home_view(request):
    read_csv_data()

    # Path that we are going to take.
    solution = []
    submit_form = SubmitForm()
    if request.method == 'POST':
        submit_form = SubmitForm(request.POST)
        if submit_form.is_valid():
            nodes = create_nodes(
                submit_form.cleaned_data.get('lat'),
                submit_form.cleaned_data.get('long')
            )
            matrix, matrix_time = construct_distance_matrix(nodes)
            print('It took %dms to construct distance matrix' % matrix_time)
            print("Matrix contains %d nodes" % len(nodes))
            total_distance, solution = TSP(matrix, nodes)
            print("Total distance travelled: %f" % total_distance)
            beers = get_beers(solution)
            
    data = {
        "solution": solution,
        "form": submit_form,
        "distance_travelled": round(total_distance),
        "beers": beers,
        "beer_count": len(beers)
    }
    return render(request, 'home.html', data)