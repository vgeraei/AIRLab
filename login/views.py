from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Member, DateTimeLog
import datetime, json
import csv
# Create your views here.


def login(request):
    members = Member.objects.all()
    now = datetime.datetime.now()
    return render(request, "login.html",{'members': members, 'now': now})

@csrf_exempt
def log(request):
    if request.method == 'POST':
        user_id = int(request.POST.get('data', None))
        if user_id:
            user = Member.objects.get(id=user_id)
            if user.is_logedin:
                user.is_logedin = False
                logout_time = DateTimeLog(date_time=datetime.datetime.now())
                logout_time.save()
                user.logout_date.add(logout_time)
            else:
                user.is_logedin = True
                login_time = DateTimeLog(date_time=datetime.datetime.now())
                login_time.save()
                user.login_date.add(login_time)
            user.save()
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


def show_info(request, member_id):

    login_list = []
    member_id = int(member_id)
    member = Member.objects.get(id=member_id)
    # member.last_duration()
    # member.auto_logout()
    logins = member.login_date.all()
    logouts = member.logout_date.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['Login', 'Logout', 'Duration'])
    rows = len(logins)

    if len(logins) == len(logouts):
        for l in range(0, rows):
            writer.writerow([logins[l].date_time, logouts[l].date_time, logouts[l].date_time-logins[l].date_time])

    return response


def face_detector(request):
    return render(request, "login.html")