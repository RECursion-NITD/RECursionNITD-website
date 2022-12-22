from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import Events_Calendar
from .forms import Eventsform, SearchForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from user_profile.models import *
from django.db.models import Q
from difflib import SequenceMatcher
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from dateutil.relativedelta import relativedelta
from . import utils

json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if isinstance(obj, datetime) else None)

pagination_per_page = 9


def get_event_duration(start_time, end_time):
    delta = relativedelta(end_time, start_time)
    attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']

    def human_readable(time_delta: relativedelta):
        return ['%d %s' % (getattr(time_delta, attr), attr if getattr(time_delta, attr) > 1 else attr[:-1])
                for attr in attrs if getattr(time_delta, attr)]

    # human_readable = lambda delta: ['%d %s' % (getattr(delta, attr), attr if getattr(delta, attr) > 1 else attr[:-1])
    #                                 for attr in attrs if getattr(delta, attr)]
    dur = human_readable(delta)
    duration = ' '.join([str(elem) for elem in dur])
    return duration


def list_events(request):
    perms = False
    search_query = request.GET.get('q')

    if request.user.is_authenticated:
        current_user_profile = Profile.objects.get(user=request.user)
        if current_user_profile.role == '1' or current_user_profile.role == '2':
            perms = True

    search = SearchForm(request.GET or None)

    events_count = {'Total': Events_Calendar.objects.all().count()}
    current_year = datetime.now().year
    year_list = list(range(current_year, current_year - 6, -1))
    for year in year_list:
        event_count_year = Events_Calendar.objects.filter(start_time__year=year).count()
        if event_count_year > 0:
            events_count[str(year)] = event_count_year

    events = Events_Calendar.objects.all().order_by('-start_time')

    if search_query:
        events = utils.search_event(events, search_query)
    paginator = Paginator(events, pagination_per_page)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
    args = {'form_search': search, 'perms': perms, 'events': events_list, 'events_count': events_count}
    if request.is_ajax():
        return render(request, 'events_list.html', args)
    return render(request, 'events_calendar.html', args)


@login_required
def create_event(request):
    perms = False
    profile = Profile.objects.get(user=request.user)
    if profile.role == '1' or profile.role == '2':
        perms = True

    form = Eventsform(request.POST or None, request.FILES)
    if request.method == 'POST' and perms == True:
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.duration = get_event_duration(f.start_time, f.end_time)
            f.save()
            return redirect('events_calendar:list_events')

        if form.errors:
            return render(request, 'event_form.html', {'form': form, 'perms': perms})

    return render(request, 'event_form.html', {'form': form, 'perms': perms})


@login_required
def event_update(request, event_id):
    try:
        event = get_object_or_404(Events_Calendar, pk=event_id)
    except:
        return render(request, 'id_error.html', {'event': 1})

    perms = False

    profile = Profile.objects.get(user=request.user)
    if profile.role == '1' or profile.role == '2':
        perms = True

    if request.method == 'POST' and perms == True:
        form = Eventsform(request.POST or None, request.FILES, instance=event)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.duration = get_event_duration(f.start_time, f.end_time)
            f.save()
            return redirect('events_calendar:list_events')

        if form.errors:
            return render(request, 'event_form.html', {'form': form, 'perms': perms})
    else:
        form = Eventsform(request.POST or None, instance=event)

    return render(request, 'event_form.html', {'form': form, 'perms': perms})


def event_detail(request, event_id):
    perms = False
    if request.user.is_authenticated:
        current_user_profile = Profile.objects.get(user=request.user)
        if current_user_profile.role == '1' or current_user_profile.role == '2':
            perms = True

    try:
        event = get_object_or_404(Events_Calendar, pk=event_id)
    except:
        return render(request, 'id_error.html', {'event': 1})
    args = {'event': event, 'perms': perms}
    return render(request, 'event_details.html', args)


def filter_event(request, type):
    perms = False
    search_query = request.GET.get('q')

    if request.user.is_authenticated:
        current_user_profile = Profile.objects.get(user=request.user)
        if current_user_profile.role == '1' or current_user_profile.role == '2':
            perms = True

    search = SearchForm(request.GET or None)

    if type not in ['Contest', 'Class', 'Event']:
        return render(request, 'id_error.html', {'event_filter': 1, 'event': 1})

    events = Events_Calendar.objects.filter(event_type=type)
    events = events.order_by('-start_time')
    events_count = {'Total': events.count()}
    current_year = datetime.now().year
    year_list = list(range(current_year, current_year - 6, -1))
    for year in year_list:
        event_count_year = events.filter(start_time__year=year).count()
        if event_count_year > 0:
            events_count[str(year)] = event_count_year
    if search_query:
        events = utils.search_event(events, search_query)
    paginator = Paginator(events, pagination_per_page)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
    event_type = type + 's' if type != 'Class' else type + 'es'
    args = {'form_search': search, 'perms': perms, 'events': events_list, 'events_count': events_count,
            'event_type': event_type}
    if request.is_ajax():
        return render(request, 'events_list.html', args)
    return render(request, 'events_calendar.html', args)