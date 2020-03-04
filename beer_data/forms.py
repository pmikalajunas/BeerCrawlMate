from django import forms


# Form consists of latitude and longitude input and ...
# dropdown selection of available algorithms to perform search.
class SubmitForm(forms.Form):
    lat = forms.FloatField()
    long = forms.FloatField()
    # Algorithm selection that will be displayed in form.
    algorithms = (
        ('Nearest Neighbour', 'Nearest Neighbour'),
        ('Simulated Annealing', 'Simulated Annealing'),
        ('Christofides', 'Christofides'),
    )
    algorithm = forms.ChoiceField(choices=algorithms)
