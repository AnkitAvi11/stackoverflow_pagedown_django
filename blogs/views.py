from django.shortcuts import render

from .models import Blog

from django import forms
from pagedown.widgets import PagedownWidget

class MyForm(forms.Form) : 
    body = forms.CharField(widget=PagedownWidget())

# Create your views here.
def addBlog (request) : 
    if request.method == 'POST' : 
        pass
    else : 
        return render(request, 'addblog.html', {'form' : MyForm})