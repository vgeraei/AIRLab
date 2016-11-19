from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Sensor(models.Model):
    data = models.CharField(max_length=10, null=True, blank=True, default=0)

    Sensors = (
        (Tempreture, 'TMP'),
        (Humidity, 'HUM'),
        (Door_status, 'DST'),
        (Window_status, 'WST'),
        (PIR, 'PIR'),
        (Luminance,'LUM')
    )
    name = models.CharField(max_length=10, choices=Sensors)

    time = models.DateTimeField(auto_now_add=True, blank=True)