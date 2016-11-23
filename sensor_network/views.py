from django.shortcuts import render
from django.http import HttpResponse
from sensor_network.models import *
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def view_home(request):
    print("Welcome Home!")
    return render(request, 'sensors.html')

def change_number(request, num):
    return HttpResponse('Number of people has successfully changed')


@csrf_exempt
def save_test(request):
    if request.method == "POST":
        print("save_test is called!")
        my_object = Sensor.objects.create(data=4, name='lum')
        my_object.save()
        return HttpResponse(status=200)
