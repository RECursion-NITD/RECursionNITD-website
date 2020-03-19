import urllib.request
import datetime
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from datetime import datetime
from django.utils.safestring import mark_safe
from .forms import *
from .models import *
from .utils import Calendar
from django.utils import timezone
import json
from datetime import date
import calendar
from django.urls import reverse


def convert24(str1):

    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]

    # remove the AM
    elif str1[-2:] == "AM":
        return str1[:-2]

    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]

    else:

        return str(int(str1[:2]) + 12) + str1[2:8]


def time_difference(time_start, time_end):

    start = datetime.strptime(time_start, "%H%M")
    end = datetime.strptime(time_end, "%H%M")
    difference = end - start
    minutes = difference.total_seconds() / 60
    return int(minutes)


def add_time(time_start, minutes):

    start = datetime.strptime(time_start, "%H%M")
    end = start + timedelta(minutes=minutes)
    return end


class CalendarView(generic.ListView):
    model = Events
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        start_date = timezone.now()
        end_date = start_date + timedelta(days=30) #Using this to display events with dates within next 30 days
        context['events_display'] = Events.objects.filter(date__range=[start_date, end_date]).order_by('date') #Collecting the most recent upcoming events to display below the calendar
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event_detail(request, event_id=None):
    try:
        instance = get_object_or_404(Events, pk=event_id)
    except:
        return HttpResponse("Id Does Not Exist!")
    return render(request, 'cal/event.html', {'event': instance})


json.JSONEncoder.default = lambda self,obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)

def superuser_only(function):
   def _inner(request, *args, **kwargs):
       if not request.user.is_superuser:
           raise PermissionDenied
       return function(request, *args, **kwargs)
   return _inner

@superuser_only
def events(request):
    events=Events.objects.all()
    perms=0
    if request.user.is_superuser:
        perms=1

    form = Eventsform(request.POST or None)

    form = Eventsform(None)
    return render(request, 'events.html',{'form':form,'events': events,"perms":perms})

@superuser_only
def event_create(request):
    perms=0
    if request.user.is_superuser:
        perms=1

    form = Eventsform(request.POST or None)
    #import pdb;pdb.set_trace();
    if form.is_valid():

        event=form.save(commit=False)
        image_url=form.cleaned_data['image_url']
        type=valid_url_extension(image_url)
        full_path='media/images/'+'event_'+str(id)+ '.png'
        try:
            urllib.request.urlretrieve(image_url,full_path)
        except:
            return HttpResponse("Downloadable Image Not Found!")
        event.image='../'+full_path
        event.save()
        return redirect('events')

    return render(request, 'create_event.html',{'form':form,"perms":perms})

@superuser_only
def event_update(request,id):
    print("call")
    try:
        event =get_object_or_404(Events, pk=id)

    except:
        return HttpResponse("id does not exist")
    else:
        perms=0
        if request.user.is_superuser:
            perms=1
        else:
            return HttpResponse("Go get perms,only admins")
        upform = Eventsform(request.POST or None, instance=event)

        if request.method == "POST":
            if upform.is_valid():

                event=upform.save(commit=False)
                image_url=upform.cleaned_data['image_url']
                type=valid_url_extension(image_url)
                full_path='media/images/'+'event_'+str(id)+ '.png'
                try:
                    urllib.request.urlretrieve(image_url,full_path)
                except:
                    return HttpResponse("Downloadable Image Not Found!")
                event.image='../'+full_path
                event.save()
                return redirect('events')
        return render(request, 'update_event.html',{'upform':upform,"perms":perms})

@superuser_only
def upcoming_events(request):
    today=timezone.now()
    upto=today + timedelta(days=365)
    events=Events.objects.filter(start_time__range=[today, upto])
    perms=0
    if request.user.is_superuser:
        perms=1
    form = Eventsform(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('events')
    form = Eventsform(None)
    return render(request, 'events.html',{'form':form,'events': events,"perms":perms,})

def calender(request):
    events=Events.objects.all().order_by('-start_time')
    args={'events':events,}
    return render(request, 'calender.html', args)