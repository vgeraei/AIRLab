from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def view_home(request):
    return render(request, 'sensors.html')

def change_number(request, num):
    return HttpResponse('Number of people has successfully changed')

def print_hello():
    print("hello")