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
        for item in f2:
            if Tags.objects.filter(name=item.name).exists():
                q_id = f.id
                t_id = Tags.objects.get(name=item.name).id
            else:
                item.save()
                q_id=f.id
                t_id=item.id
            if Taggings.objects.filter(question=Questions.objects.get(pk=q_id), tag=Tags.objects.get(pk=t_id)).exists():
                continue
            else:
                tagging_add(q_id, t_id)
    if form.is_valid():
        return redirect('list_questions')

    return render(request, 'recursion_website/questions-form.html', {'form': form,'form2':form2,})

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
        question =get_object_or_404( Questions,pk=id)
    except:
        return HttpResponse("id does not exist")
    else:
        form = Questionform(request.POST or None, instance=question)
        Tagform = modelformset_factory(Tags, fields=('name',), extra=1)
        if request.method == 'POST':
            form2 = Tagform(request.POST or None)
        else:
            question = Questions.objects.get(pk=id)
            list=Taggings.objects.filter(question=Questions.objects.get(pk=id))
            table=Tags.objects.none()
            for instance in list:
                item=Tags.objects.filter(pk=instance.tag.id)
                table=table|item
            form2 = Tagform(queryset=table)
        if form.is_valid():
            f = form.save(commit=False)
            f.user_id = request.user
            form.save()
        if form2.is_valid():
            f2 = form2.save(commit=False)
            for item in f2:
                print(item)
                print(item.name)
                print(item.id)
                if item.id == None:
                    if Tags.objects.filter(name=item.name).exists():
                        q_id = f.id
                        t_id = Tags.objects.get(name=item.name).id
                    else:
                        item.save()
                        q_id = f.id
                        t_id = item.id
                    if Taggings.objects.filter(question=Questions.objects.get(pk=q_id), tag=Tags.objects.get(pk=t_id)).exists():
                        continue
                    else:
                        tagging_add(q_id, t_id)
                else:
                   to_del = Taggings.objects.get(question=Questions.objects.get(pk=f.id), tag=Tags.objects.get(pk=item.id))
                   print(Tags.objects.get(pk=item.id).name)
                   to_del.delete()
                   if item.name ==None:
                       continue
                   if Tags.objects.filter(name=item.name).exists():
                       q_id = f.id
                       t_id = Tags.objects.get(name=item.name).id
                   else:
                       obj=Tags.objects.create(name=item.name)
                       obj.save()
                       print(obj.name)
                       print(obj.id)
                       q_id = f.id
                       t_id =obj.id
                   if Taggings.objects.filter(question=Questions.objects.get(pk=q_id), tag=Tags.objects.get(pk=t_id)).exists():
                       continue
                   else:
                       tagging_add(q_id, t_id)
        if form.is_valid():
            return redirect('list_questions')

    return render(request, 'recursion_website/questions-form.html', {'form': form, 'form2': form2, 'question': question})