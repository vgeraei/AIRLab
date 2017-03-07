from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from sensor_network.models import *
from django.views.decorators.csrf import csrf_exempt
import json
import serial
import signal
import os

# from .tasks import print_it
# from celery import group




# Create your views here.
def view_home(request):
    print("Welcome Home!")
    return render(request, 'sensors.html')

def change_number(request, num):
    return HttpResponse('Number of people has successfully changed')

def switch_lights_off(request):
    print("Lights off!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    with open('recPID', 'r') as f:
        pid = int(f.readline())

    print 'My PID is:', pid
    os.kill(pid, signal.SIGUSR2)


    # print("Lights off!")
    return HttpResponse(status=200)

def switch_lights_on(request):
    print("Lights on!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    with open('recPID', 'r') as f:
        pid = int(f.readline())

    print 'My PID is:', pid
    os.kill(pid, signal.SIGUSR1)
    return HttpResponse(status=200)

@csrf_exempt
def query_tmp(request):
    if request.method == "POST":
        print("query request done!")
        #data_map = {'name': 'DST'}
        dst = Sensor.objects.raw('SELECT * FROM sensor_network_sensor WHERE name = %s limit 10000', ['DST'])
        tmp = Sensor.objects.raw('SELECT * FROM sensor_network_sensor WHERE name = %s limit 10000', ['TMP'])
        pir = Sensor.objects.raw('SELECT * FROM sensor_network_sensor WHERE name = %s limit 10000', ['PIR'])
        hum = Sensor.objects.raw('SELECT * FROM sensor_network_sensor WHERE name = %s limit 10000', ['HUM'])
        lum = Sensor.objects.raw('SELECT * FROM sensor_network_sensor WHERE name = %s limit 10000', ['LUM'])
        #data = Sensor.objects.raw('SELECT * FROM    TABLE WHERE   ID = (SELECT MAX(ID)  FROM TABLE)')
        dst1 = 0
        dst0 = 0
        if len(list(dst)) > 0:
            for d in dst:
                if d.data == "1":
                    dst1 = dst1 + 1
                else:
                    dst0 = dst0 + 1

        return JsonResponse({'dst0': dst0, 'dst1': dst1})


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
        with open('realtime_data.json') as json_data:
            realtime_json = json.load(json_data)
        return HttpResponse(realtime_json, content_type='application/json')
