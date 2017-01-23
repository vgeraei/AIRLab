from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from sensor_network.models import *
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def view_smart_tile(request):
    print("Smart tile is loaded!")
    return render(request, 'smart_tile.html')