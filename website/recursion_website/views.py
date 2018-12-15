from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from  .forms import *
from django.conf import settings
from .models import *
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse
from django.template import loader, RequestContext

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


@csrf_exempt
def add_question(request):
    form = Questionform(request.POST or None)
    if form.is_valid():
       f = form.save(commit=False)
       f.user_id = request.user
       f.save()
       return redirect('questions')

    return render(request, 'recursion_website/questions-form.html', {'form': form})

def list_questions(request):
    questions = Questions.objects.all()
    answers=Answers.objects.all()
    follows=Follows.objects.all()
    tags=Tags.objects.all()
    taggings=Taggings.objects.all()
    args = {'questions':questions, 'answers':answers, 'follows':follows, 'tags':tags, 'taggings':taggings}

    return render(request, 'recursion_website/questions.html', args)


def detail_questions(request, id):
    try:
        questions =get_object_or_404( Questions,pk=id)
    except:
        return HttpResponse("id does not exist")
    answers = Answers.objects.all()
    follows = Follows.objects.all()
    tags = Tags.objects.all()
    taggings = Taggings.objects.all()
    upvotes=Upvotes.objects.all()
    comments=Comments.objects.all()
    args = {'questions': questions, 'answers': answers, 'follows': follows, 'tags':tags, 'taggings':taggings, 'upvotes':upvotes, 'comments':comments }

    return render(request, 'recursion_website/detail.html', args)

@login_required
def update_questions(request, id):
    try:
        questions =get_object_or_404( Questions,pk=id)
    except:
        return HttpResponse("id does not exist")



    return render(request, 'recursion_website/questions-form.html', { 'questions': questions})  

