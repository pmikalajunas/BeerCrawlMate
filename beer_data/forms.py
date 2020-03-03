from django import forms

class SubmitForm(forms.Form):
    lat = forms.FloatField()
    long = forms.FloatField()
    algorithms = (
        ('Nearest Neighbour', 'Nearest Neighbour'),        
        ('Simulated Annealing', 'Simulated Annealing'),
        ('Christofides', 'Christofides'),
    )
    algorithm = forms.ChoiceField(choices=algorithms)
