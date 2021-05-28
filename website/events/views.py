from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader, RequestContext
from .forms import Eventsform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from itertools import chain
from django.utils import timezone
from datetime import timedelta
from django.core.files.base import ContentFile
from io import BytesIO
import urllib.request
from PIL import Image
import json
from datetime import datetime
from .validators import valid_url_extension
from .validators import valid_url_mimetype
from django.core.exceptions import PermissionDenied

json.JSONEncoder.default = lambda self,obj: (obj.isoformat() if isinstance(obj, datetime) else None)


def superuser_only(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner


@superuser_only
def events(request):
    qs=Events.objects.all()
    perms=0
    if request.user.is_superuser:
        perms=1

    form = Eventsform(None)
    return render(request, 'events.html',{'form':form,'events': qs,"perms":perms})


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
        full_path = 'media/images/'+'event_'+datetime.strftime(datetime.now(),"%Y-%m-%dT%H-%M-%S-%f") + '.png'
        try:
            urllib.request.urlretrieve(image_url,full_path)
        except:
            return HttpResponse("Downloadable Image Not Found!")
        event.image='../'+full_path
        event.save()
        return redirect('events:events')

    return render(request, 'create_event.html',{'form':form,"perms":perms})


@superuser_only
def event_detail(request,event_id):
    try:
        event =get_object_or_404( Events,pk=event_id)
    except:
        return HttpResponse("id does not exist")
    else:
        return render(request,'event_detail.html',{'event':event})


@superuser_only
def event_update(request,event_id):
    print("call")
    try:
        event =get_object_or_404(Events, pk=event_id)

    except Events.DoesNotExist:
        return HttpResponse("id does not exist")
    else:
        if request.user.is_superuser:
            perms=1
        else:
            return HttpResponse("Go get perms,only admins")
        upform = Eventsform(request.POST or None, instance=event)

        if request.method == "POST":
            if upform.is_valid():

                event=upform.save(commit=False)
                image_url=upform.cleaned_data['image_url']
                full_path = 'media/images/event_' + datetime.strftime(datetime.now(),"%Y-%m-%dT%H-%M-%S-%f") + '.png'
                try:
                    urllib.request.urlretrieve(image_url,full_path)
                except:
                    return HttpResponse("Downloadable Image Not Found!")
                event.image='../'+full_path
                event.save()
                return redirect('events:events')
        return render(request, 'update_event.html',{'upform':upform,"perms":perms})


@superuser_only
def upcoming_events(request):
    today=timezone.now()
    upto=today + timedelta(days=365)
    qs=Events.objects.filter(start_time__range=[today, upto])
    perms=0
    if request.user.is_superuser:
        perms=1
    form = Eventsform(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('events:events')
    form = Eventsform(None)
    return render(request, 'events.html',{'form':form,'events': qs,"perms":perms,})


def calender(request):
    qs=Events.objects.all().order_by('-start_time')
    args={'events':qs,}
    return render(request, 'calender.html', args)