from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from sensor_network.models import *
from django.views.decorators.csrf import csrf_exempt
import json
import serial

# from .tasks import print_it
# from celery import group




# Create your views here.
def view_home(request):
    print("Welcome Home!")
    return render(request, 'SensorUI.html')

def change_number(request, num):
    return HttpResponse('Number of people has successfully changed')

def switch_lights_off(request):
    print("Lights off!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    raw_msg = "7E 00 0F 10 01 00 13 A2 00 40 C8 E5 22 FF FE 00 00 30 FD"
    msg = "".join(raw_msg.split())
    msg = msg.decode("hex")

    PORT = '/dev/ttyUSB'
    BAUD_RATE = 9600
    # Open serial port
    usb_counter = 0

    while True:
        try:
            ser = serial.Serial(PORT + str(usb_counter), BAUD_RATE)
            # print("connected")
            break
        except:
            # print(usb_counter)
            usb_counter = usb_counter + 1

    ser.write(msg)
    ser.close()

    # print("Lights off!")
    return HttpResponse(status=200)

def switch_lights_on(request):
    print("Lights on!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    raw_msg = "7E 00 0F 10 01 00 13 A2 00 40 C8 E5 22 FF FE 00 00 31 FC"
    msg = "".join(raw_msg.split())
    msg = msg.decode("hex")

    PORT = '/dev/ttyUSB'
    BAUD_RATE = 9600
    # Open serial port
    usb_counter = 0

    while True:
        try:
            ser = serial.Serial(PORT + str(usb_counter), BAUD_RATE)
            # print("connected")
            break
        except:
            # print(usb_counter)
            usb_counter = usb_counter + 1

    ser.write(msg)
    ser.close()
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
        print("request realtime data:")
        with open('realtime_data.json') as json_data:
            realtime_json = json.load(json_data)
        return HttpResponse(realtime_json, content_type='application/json')
