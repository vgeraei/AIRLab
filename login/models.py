from __future__ import unicode_literals

from django.db import models


class DateTimeLog(models.Model):
    date_time = models.DateTimeField()


class Member(models.Model):
    name = models.CharField(max_length=20)
    # position = models.CharField(max_length=100)
    login_date = models.ManyToManyField(DateTimeLog, related_name="login")
    logout_date = models.ManyToManyField(DateTimeLog, related_name="logout")
    is_logedin = models.BooleanField(default=False)

    def __str__(self):
        return self.name
