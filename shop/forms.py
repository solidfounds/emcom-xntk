__author__ = 'seader'
from django import forms



class SearchForm(forms.Form):
    buscar = forms.CharField()
    pass
