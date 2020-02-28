from django.shortcuts import render
from django.http import HttpResponse

from beer_data.csv_reader import *
from beer_data.data_processor import *

def home_view(request):

    read_csv_data()
    matrix, matrix_time = construct_distance_matrix(51.355468, 11.100790)
    print('It took %dms to construct distance matrix' % matrix_time)
    data = {
        
    }
    return render(request, 'home.html', data)