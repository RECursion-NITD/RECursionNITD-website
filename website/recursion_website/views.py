from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from  .forms import *
from django.conf import settings
from .models import *
from django.contrib.auth.models import User

@csrf_exempt
def add_question(request):
    form = Questionform(request.POST or None)
    if form.is_valid():
       f = form.save(commit=False)
       f.user_id = request.user
       f.save()
       return redirect('questions')

    return render(request, 'questions-form.html', {'form': form})

def questions(request):
    return HttpResponse("heelo world")   
