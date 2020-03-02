from django.shortcuts import render
from django.http import HttpResponse

from beer_data.csv_reader import *
from beer_data.data_processor import *
from beer_data.forms import SubmitForm

from beer_data.solution import Solution
from beer_data.util import validate_coordinates


# Main view that displays map and tables.
# There is a form to put coordinates for search.
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
            if validate_coordinates(home_lat, home_long):
                solution = Solution.retrieve_solution(home_lat, home_long)
            
    data = {
        "solution": solution,
        "form": submit_form
    }
    return render(request, 'home.html', data)