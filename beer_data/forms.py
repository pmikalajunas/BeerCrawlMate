from django import forms

class SubmitForm(forms.Form):
    lat = forms.FloatField()
    long = forms.FloatField()
