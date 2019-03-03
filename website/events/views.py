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
import datetime
from .validators import valid_url_extension
from .validators import valid_url_mimetype

json.JSONEncoder.default = lambda self,obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)


def events(request):
    events=Events.objects.all()
    perms=0
    if request.user.is_superuser:
        perms=1

    form = Eventsform(request.POST or None)
    if form.is_valid():
        f = form.save()
        id = f.id
        event = Events.objects.get(pk=id)
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

    form = Eventsform(None)
    return render(request, 'events.html',{'form':form,'events': events,"perms":perms})

def event_create(request):
    perms=0
    if request.user.is_superuser:
        perms=1

    form = Eventsform(request.POST or None)
    if request.POST.get('ajax_check') == "True" :

        if form.is_valid():
            title=request.POST.get('title')
            f=form.save()
            print(f.id)
            Id=f.id
            return HttpResponse(json.dumps({
            'title':title,
            'description':f.description,
            'image_url':f.image_url,
            'start_time':f.start_time,
            'end_time':f.end_time,
            "id":Id,
            'Success':"Success"
            }))
        form = Eventsform(None)
        return HttpResponse('Invalid')
    return render(request, 'create_event.html',{'form':form,"perms":perms})

def event_detail(request,id):
    try:
        event =get_object_or_404( Events,pk=id)
    except:
        return HttpResponse("id does not exist")
    else:
        return render(request,'event_detail.html',{'event':event})

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
        print("out")
        print(upform)
        if request.method == "POST":

            if request.user :  #of no use

                if upform.is_valid():

                    f=upform.save()
                    id = event.id
                    image_url = form.cleaned_data['image_url']
                    type = valid_url_extension(image_url)
                    full_path = 'media/images/' + 'event_' + str(id) + '.png'
                    try:
                        urllib.request.urlretrieve(image_url, full_path)
                    except:
                        return HttpResponse("Downloadable Image Not Found!")
                    event.image = '../' + full_path
                    event.save()
                    Id=f.id
                    title=f.title
                    return HttpResponse(json.dumps({
                    'title':title,
                    'description':f.description,
                    'image_url':f.image_url,
                    'start_time':f.start_time,
                    'end_time':f.end_time,
                    "id":Id,
                    'Success':"Success"
                    }))
                return HttpResponse("Invalid")
        return render(request, 'update_event.html',{'upform':upform,"perms":perms})

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
