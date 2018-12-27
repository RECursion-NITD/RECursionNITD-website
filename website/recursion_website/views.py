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
from itertools import chain

# Create your views here.

def tagging_add(q_id, t_id):
    p = Taggings.objects.create(question=get_object_or_404(Questions, pk=q_id), tag=get_object_or_404(Tags, pk=t_id))
    return

def bulk_tagging_add(question, tags):
    taggings = []
    for tag in tags:
        taggings.append(Taggings(question=question, tag=tag))
    Taggings.objects.bulk_create(taggings)
    return

@login_required
def add_question(request):
    form = Questionform(request.POST or None)

    Tagform = modelformset_factory(Tags, fields=('name',), extra=5)
    if request.method=='POST':
         form2 = Tagform(request.POST)
    else:
         form2 = Tagform(queryset=Tags.objects.none())
    if form.is_valid():
        f = form.save(commit=False)
        f.user_id = request.user
        form.save()
    if form2.is_valid():
        f2 = form2.save(commit=False)
        tagging_list = []
        for item in f2:
            if Tags.objects.filter(name=item.name).exists():
                tag = Tags.objects.get(name=item.name)
            else:
                item.save()
                tag=item
            if tag not in tagging_list:
                tagging_list.append(tag)

        bulk_tagging_add(f, tagging_list)  # use a bulk create function which accepts a list
    if form.is_valid():
        return redirect('list_questions')

    return render(request, 'questions-form.html', {'form': form,'form2':form2,})

def list_questions(request):
    questions = Questions.objects.all()
    answers=Answers.objects.all()
    follows=Follows.objects.all()
    tags=Tags.objects.all()
    taggings=Taggings.objects.all()
    args = {'questions':questions, 'answers':answers, 'follows':follows, 'tags':tags, 'taggings':taggings}
    return render(request, 'questions.html', args)

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
    user = request.user
    flag=0
    if Follows.objects.filter(question=questions, user=user).exists():
        flag=1
    args = {'questions': questions, 'answers': answers, 'follows': follows, 'tags':tags, 'taggings':taggings, 'upvotes':upvotes, 'comments':comments , 'flag':flag }
    return render(request, 'detail.html', args)

@login_required
def update_questions(request, id):
    try:
        question = get_object_or_404(Questions, pk=id)
    except:
        return HttpResponse("id does not exist")

    form = Questionform(request.POST or None, instance=question)
    Tagform = modelformset_factory(Tags, fields=('name',), extra=1)
    if request.method == 'POST':
        form2 = Tagform(request.POST or None)
        if form.is_valid():
            f = form.save(commit=False)
            f.user_id = request.user
            form.save()
        if form2.is_valid():
            to_del = Taggings.objects.filter(question=question)  # delete all prev taggings
            if to_del.exists():
                to_del.delete()
            tagging_list = []
            for item in form2:  # create new taggings
                if item.cleaned_data.get("name") != None:  # if a tag was removed
                    try:
                        tag_name = item.cleaned_data.get('name')
                        tag = get_object_or_404(Tags, name=tag_name)  # see if tag exists
                    except:
                        tag = Tags.objects.create(name=tag_name)  # if not create

                    if tag not in tagging_list:
                        tagging_list.append(tag)

            bulk_tagging_add(question, tagging_list)  # use a bulk create function which accepts a list
            return redirect('list_questions')
    else:
        question = Questions.objects.get(pk=id)
        id_list = Taggings.objects.filter(question=question).values('tag_id')  # get all tag ids from taggings
        id_list = [id['tag_id'] for id in id_list]  # convert the returned dictionary list into a simple list
        form2 = Tagform(queryset=Tags.objects.filter(id__in=id_list))  # populate form with tags

        return render(request, 'questions-form.html', {'form': form, 'form2': form2, 'question': question})

@login_required
def edit_following(request, id):
    try:
        question =get_object_or_404( Questions,pk=id)
    except:
        return HttpResponse("id does not exist")
    user = request.user
    if user != question.user_id:
       if Follows.objects.filter(question=question, user=user).exists():
           follow = Follows.objects.get(question=question, user=user)
           follow.delete()
       else:
           follow = Follows.objects.create(question=question, user=user)
           follow.save()
    return redirect('list_questions')
