from django.shortcuts import render
from django.http import HttpResponse
from sensor_network.models import *
from django.views.decorators.csrf import csrf_exempt
import sensor_network.recieve_data
import json



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

@csrf_exempt
def load_realtime_data(request):
    if request.method == "POST":
        # print("request realtime data:")
        realtime_json = json.dumps(sensor_network.recieve_data.realtime_data)
        return HttpResponse(realtime_json, content_type='application/json')
