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

# Create your views here.

def tagging_add(q_id, t_id):
    p = Taggings.objects.create(question=get_object_or_404(Questions, pk=q_id), tag=get_object_or_404(Tags, pk=t_id))
    return

@login_required
def add_question(request):
    form = Questionform(request.POST or None)
    f = form.save(commit=False)
    form2 = Tagsform(request.POST or None)
    f2 = form2.save(commit=False)
    form3 = Tagsform(request.POST or None)
    f3 = form3.save(commit=False)
    form4 = Tagsform(request.POST or None)
    f4 = form4.save(commit=False)
    form5 = Tagsform(request.POST or None)
    f5 = form5.save(commit=False)
    form6 = Tagsform(request.POST or None)
    f6 = form6.save(commit=False)
    array = request.POST.getlist('name')
    print(array)
    count=1
    for arr in array:
        if count==1:
            f2.name=arr
        elif count==2:
            f3.name=arr
        elif count==3:
            f4.name=arr
        elif count==4:
            f5.name=arr
        elif count==5:
            f6.name=arr
        count+=1

    if form.is_valid():
       f.user_id = request.user
       f.save()

    if f2.name != '' and form2.is_valid():
       list=Tags.objects.all()
       flag=0
       pos=0
       for item in list:
           if item.name==f2.name:
               flag=1
               pos=item.id
       if flag==1:
           t2_id = pos
       elif flag==0:
           f2.save()
           t2_id = f2.id
       q2_id = f.id
       tagging_add(q2_id, t2_id)

    if f3.name !='' and form3.is_valid():
        list = Tags.objects.all()
        flag = 0
        pos = 0
        for item in list:
            if item.name == f3.name:
                flag = 1
                pos = item.id
        if flag == 1:
            t3_id = pos
        elif flag == 0:
            f3.save()
            t3_id = f3.id
        q3_id = f.id
        tagging_add(q3_id, t3_id)

    if f4.name !='' and form4.is_valid():
        list = Tags.objects.all()
        flag = 0
        pos = 0
        for item in list:
            if item.name == f4.name:
                flag = 1
                pos = item.id
        if flag == 1:
            t4_id = pos
        elif flag == 0:
            f4.save()
            t4_id = f4.id
        q4_id = f.id
        tagging_add(q4_id, t4_id)

    if f5.name !='' and form5.is_valid():
        list = Tags.objects.all()
        flag = 0
        pos = 0
        for item in list:
            if item.name == f5.name:
                flag = 1
                pos = item.id
        if flag == 1:
            t5_id = pos
        elif flag == 0:
            f5.save()
            t5_id = f5.id
        q5_id = f.id
        tagging_add(q5_id, t5_id)

    if f6.name !='' and form6.is_valid():
        list = Tags.objects.all()
        flag = 0
        pos = 0
        for item in list:
            if item.name == f6.name:
                flag = 1
                pos = item.id
        if flag == 1:
            t6_id = pos
        elif flag == 0:
            f6.save()
            t6_id = f6.id
        q6_id = f.id
        tagging_add(q6_id, t6_id)

    if form.is_valid():
         return redirect('list_questions')

    return render(request, 'questions-form.html', {'form': form,'form2':form2, 'form3': form3 , 'form4': form4 , 'form5': form5 , 'form6': form6})

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
    args = {'questions': questions, 'answers': answers, 'follows': follows, 'tags':tags, 'taggings':taggings, 'upvotes':upvotes, 'comments':comments }
    return render(request, 'detail.html', args)

@login_required
def update_questions(request, id):
    try:
        question =get_object_or_404( Questions,pk=id)
    except:
        return HttpResponse("id does not exist")
    else:
        form = Questionform(request.POST or None, instance=question)

        if form.is_valid():
            form.save()
            return redirect('list_questions')

    return render(request, 'questions-form.html', {'form': form, 'question': question})
