from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import Events_Calendar
from .forms import Eventsform, SearchForm
from django.http import HttpResponse, HttpResponseRedirect
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

json.JSONEncoder.default = lambda self,obj: (obj.isoformat() if isinstance(obj, datetime) else None)

def list_events(request):

    perms = False
    if request.user.is_authenticated:
        current_user_profile = Profile.objects.get(user = request.user)
        if current_user_profile.role == '1' or current_user_profile.role == '2':
            perms = True
    
    search = SearchForm(request.POST or None)
    if request.method == 'POST':
        if search.is_valid():
            key_req = search.cleaned_data
            key = key_req.get('key')
            return HttpResponseRedirect(reverse('events_calendar:search_event', args=(key,)))

    events = Events_Calendar.objects.all().order_by('-start_time')
    paginator = Paginator(events, 5)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
    args = {'form_search':search, 'perms':perms, 'events': events_list}
    if request.is_ajax():
        return render(request, 'events_list.html', args)
    return render(request, 'events_calendar.html', args)

def create_event(request):
    return render(request, 'events_calendar.html', {})

def event_update(request, event_id):
    return render(request, 'events_calendar.html', {})

def event_detail(request, event_id):
    return render(request, 'events_calendar.html', {})

def search_event(request, key):

    search = SearchForm(request.POST or None)
    if request.method == 'POST':
        if search.is_valid():
            key_req = search.cleaned_data
            key = key_req.get('key')
            return HttpResponseRedirect(reverse('events_calendar:search_event', args=(key,)))

    perms = False
    if request.user.is_authenticated:
        current_user_profile = Profile.objects.get(user = request.user)
        if current_user_profile.role == '1' or current_user_profile.role == '2':
            perms = True

    events_list = Events_Calendar.objects.all()
    events_found = []
    for event in events_list:
        if SequenceMatcher(None, event.title.lower(), key.lower()).ratio() > 0.4:
            events_found.append([SequenceMatcher(None, event.title.lower(), key.lower()).ratio(), event])
        if SequenceMatcher(None, event.description.lower(), key.lower()).ratio() > 0.5:
            events_found.append([SequenceMatcher(None, event.description.lower(), key.lower()).ratio(), event])
    events = []
    events_found.sort(key=lambda x: x[0], reverse=True)
    for event in events_found:
        if event[1] not in events:
            events.append(event[1])

    paginator = Paginator(events, 5)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
    args = {'form_search':search, 'perms':perms, 'events': events_list}
    if request.is_ajax():
        return render(request, 'events_list.html', args)
    return render(request, 'events_calendar.html', args)

def filter_event(request, type):

    perms = False
    if request.user.is_authenticated:
        current_user_profile = Profile.objects.get(user = request.user)
        if current_user_profile.role == '1' or current_user_profile.role == '2':
            perms = True

    search = SearchForm(request.POST or None)
    if request.method == 'POST':
        if search.is_valid():
            key_req = search.cleaned_data
            key = key_req.get('key')
            return HttpResponseRedirect(reverse('events_calendar:search_event', args=(key,)))

    events_list = Events_Calendar.objects.all()

    if type == 'All':
       events = events_list
    else:
        events = events_list.filter(event_type=type)

    events = events.order_by('-start_time')
    
    paginator = Paginator(events, 5)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
    args = {'form_search':search, 'perms':perms, 'events': events_list}
    if request.is_ajax():
        return render(request, 'events_list.html', args)
    return render(request, 'events_calendar.html', args)