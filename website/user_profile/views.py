from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader, RequestContext
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from itertools import chain
from django.core.files.base import ContentFile
from io import BytesIO
import urllib.request
from PIL import Image

VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]

def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    end=([url.endswith(e) for e in extension_list])
    count=1
    for e in end:
        if e == True:
          if count==1:
              type=".jpg"
          elif count==2:
              type=".jpeg"
          elif count==3:
              type=".png"
          elif count==4:
              type=".gif"
        count+=1
    return type



def user_register(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        if User.objects.filter(username=['username']).exists():
            return redirect('user_register')
        form.save()
        new_user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'],
                                )
        login(request, new_user)
        return redirect('edit_profile')
    return render(request, 'register.html', {'form': form})

@login_required
def edit_profile(request):
    form= Profileform(request.POST or None)
    user=request.user
    id = user.id
    profile=get_object_or_404(Profile, user=user)
    form = Profileform(request.POST or None, instance=profile)
    if form.is_valid():
        image_url=form.cleaned_data['image_url']
        type=valid_url_extension(image_url)
        import pdb;pdb.set_trace();
        full_path='media/images/'+profile.user.username+type
        try:
            urllib.request.urlretrieve(image_url,full_path)
        except:
            return HttpResponse("Downloadable Image Not Found!")
        if profile.user==request.user:
             profile.image='../'+full_path
             form.save()
        return HttpResponseRedirect(reverse('view_profile', args=(id,)))

    return render(request, 'create.html', {'form': form,})

def view_profile(request, id):
    try:
        user=get_object_or_404(User, pk=id)
    except:
        print(request.user.id) 
        return HttpResponse("User does not exist!")
    try:
        profile=get_object_or_404(Profile, user=user)
    except:
        return HttpResponse("User has not created a Profile yet!")
        
    args = {'profile': profile,}
    return render(request, 'recursion_website/profile.html', args)
