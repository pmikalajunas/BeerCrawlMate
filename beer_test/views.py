from django.shortcuts import render

from beer_data.csv_reader import *
from beer_data.forms import SubmitForm
from beer_data.solution import Solution, retrieve_solution
from beer_data.util import validate_coordinates


# Main view that displays map and tables.
# There is a form to put coordinates for search.
from beer_test.api_key import MAPS_API_KEY


def home_view(request):
    # Reads beer data from supplied csv files, initializes DB.
    read_csv_data()

    # Path that we are going to take.
    solution = Solution()
    submit_form = SubmitForm()
    if request.method == 'POST':
        submit_form = SubmitForm(request.POST)
        if submit_form.is_valid():
            home_lat = submit_form.cleaned_data.get('lat')
            home_long = submit_form.cleaned_data.get('long')
            algorithm = submit_form.cleaned_data.get('algorithm')
            if validate_coordinates(home_lat, home_long):
                solution = retrieve_solution(home_lat, home_long, algorithm)
    data = {
        "solution": solution,
        "form": submit_form,
        "maps_api_key": MAPS_API_KEY
    }
    return render(request, 'home.html', data)