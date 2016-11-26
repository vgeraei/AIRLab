"""AIRLab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from sensor_network.views import *
from sensor_network.recieve_data import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sensors/$', view_home),
    url(r'^sensors/change_number/$', save_test),
    url(r'^sensors/load_realtime/$', load_realtime_data),
]

import subprocess
subprocess.Popen(["python", "sensor_network/recieve_data.py"])
