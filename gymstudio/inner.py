from django.shortcuts import render
from . models import *
from django.http import HttpResponse

# Create your views here.

def profile(request):
    pageTitle = 'Dashboard'

    # countries =  Country.objects.all().values_list ('id', 'name')
    # print(countries)

    context = {
        'pageTitle' : pageTitle
    }
    # return HttpResponse(countries) 
    return render(request, 'users/profile.html',context) 