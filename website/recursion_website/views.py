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

# Create your views here.

def tagging_add(q_id, t_id):
    p = Taggings.objects.create(question=get_object_or_404(Questions, pk=q_id), tag=get_object_or_404(Tags, pk=t_id))
    return

@login_required
def add_question(request):
    form = Questionform(request.POST or None)

    Tagform = modelformset_factory(Tags, fields=('name',), extra=5)
    form2 = Tagform(request.POST,  queryset=Tags.objects.none())
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
        tagging_add(q_id, t_id)
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
    args = {'questions': questions, 'answers': answers, 'follows': follows, 'tags':tags, 'taggings':taggings, 'upvotes':upvotes, 'comments':comments }
    return render(request, 'detail.html', args)


@login_required
def update_questions(request, id):
    try:
        question = get_object_or_404(Questions, pk=id)
        p = Taggings.objects.filter(question=question)
        print(p)
        boo = p.count()
        print(boo)
        if boo > 0:
            count = 1
            for k in p:
                if k.question.id == id:
                    if count == 1:
                        tag1 = get_object_or_404(Tags, pk=k.tag.id)
                    if count == 2:
                        tag2 = get_object_or_404(Tags, pk=k.tag.id)

                    if count == 3:
                        tag3 = get_object_or_404(Tags, pk=k.tag.id)
                    if count == 4:
                        tag4 = get_object_or_404(Tags, pk=k.tag.id)

                    if count == 5:
                        tag5 = get_object_or_404(Tags, pk=k.tag.id)
                    count += 1


    except:
        return HttpResponse("id does not exist")
    else:
        form = Questionform(request.POST or None, instance=question)
        if boo >= 0:
            if boo > 0:
                form2 = Tagsform(request.POST or None, instance=tag1)
            else:
                form2 = Tagsform(request.POST or None)
            if boo > 1:
                form3 = Tagsform(request.POST or None, instance=tag2)

            else:
                form3 = Tagsform(request.POST or None)
            if boo > 2:
                form4 = Tagsform(request.POST or None, instance=tag3)

            else:
                form4 = Tagsform(request.POST or None)
            if boo > 3:
                form5 = Tagsform(request.POST or None, instance=tag4)
            else:
                form5 = Tagsform(request.POST or None)
            if boo > 4:
                form6 = Tagsform(request.POST or None, instance=tag5)
            else:
                form6 = Tagsform(request.POST or None)

            f = form.save(commit=False)
            f2 = form2.save(commit=False)
            f3 = form3.save(commit=False)
            f4 = form4.save(commit=False)
            f5 = form5.save(commit=False)
            f6 = form6.save(commit=False)

            array = request.POST.getlist('name')
            print("a")
            print(array)
            count = 1
            for arr in array:
                if count == 1:
                    f2.name = arr
                elif count == 2:
                    f3.name = arr
                elif count == 3:
                    f4.name = arr
                elif count == 4:
                    f5.name = arr
                elif count == 5:
                    f6.name = arr
                count += 1
            if form.is_valid():
                f.user_id = request.user
                f.save()
            # assuming null as one of the tag
            if f2.name != '' and form2.is_valid():
                print(f2.name)
                if Tags.objects.filter(name=f2.name).exists():
                    q2_id = f.id
                    t2_id = Tags.objects.get(name=f2.name).id
                else:
                    f2.save()
                    q2_id = f.id
                    t2_id = f2.id
                if not Taggings.objects.filter(question_id=q2_id, tag_id=t2_id).exists():
                    tagging_add(q2_id, t2_id)
            else:

                print(f2.name)
                q2_id = f.id
                t2_id = f2.name
                if Taggings.objects.filter(question_id=q2_id, tag__name=t2_id).exists():
                    Taggings.objects.get(question=Questions.objects.get(pk=q2_id),
                                         tag=Tags.objects.get(name=t2_id)).delete()

            if f3.name != '' and form3.is_valid():
                if Tags.objects.filter(name=f3.name).exists():
                    q3_id = f.id
                    t3_id = Tags.objects.get(name=f3.name).id
                else:
                    f3.save()
                    q3_id = f.id
                    t3_id = f3.id
                if not Taggings.objects.filter(question_id=q3_id, tag_id=t3_id).exists():
                    tagging_add(q3_id, t3_id)
            else:

                q3_id = f.id
                t3_id = f3.name
                if Taggings.objects.filter(question_id=q3_id, tag__name=t3_id).exists():
                    Taggings.objects.filter(question=Questions.objects.get(pk=q3_id),
                                            tag=Tags.objects.get(name=t3_id)).delete()

            if f4.name != '' and form4.is_valid():
                if Tags.objects.filter(name=f4.name).exists():
                    q4_id = f.id
                    t4_id = Tags.objects.get(name=f4.name).id
                else:
                    f4.save()
                    q4_id = f.id
                    t4_id = f4.id
                if not Taggings.objects.filter(question_id=q4_id, tag_id=t4_id).exists():
                    tagging_add(q4_id, t4_id)
            else:

                q4_id = f.id
                t4_id = f4.name
                if Taggings.objects.filter(question_id=q4_id, tag__name=t4_id).exists():
                    Taggings.objects.filter(question=Questions.objects.get(pk=q4_id),
                                            tag=Tags.objects.get(name=t4_id)).delete()

            if f5.name != '' and form5.is_valid():
                if Tags.objects.filter(name=f5.name).exists():
                    q5_id = f.id
                    t5_id = Tags.objects.get(name=f5.name).id
                else:
                    f5.save()
                    q5_id = f.id
                    t5_id = f5.id
                if not Taggings.objects.filter(question_id=q5_id, tag_id=t5_id).exists():
                    tagging_add(q5_id, t5_id)
            else:

                q5_id = f.id
                t5_id = f5.name
                if Taggings.objects.filter(question_id=q5_id, tag__name=t5_id).exists():
                    Taggings.objects.filter(question=Questions.objects.get(pk=q5_id),
                                            tag=Tags.objects.get(name=t5_id)).delete()

            if f6.name != '' and form6.is_valid():
                if Tags.objects.filter(name=f6.name).exists():
                    q6_id = f.id
                    t6_id = Tags.objects.get(name=f6.name).id
                else:
                    f6.save()
                    q6_id = f.id
                    t6_id = f6.id
                if not Taggings.objects.filter(question_id=q6_id, tag_id=t6_id).exists():
                    tagging_add(q6_id, t6_id)
            else:

                q6_id = f.id
                t6_id = f6.name
                if Taggings.objects.filter(question_id=q6_id, tag__name=t6_id).exists():
                    Taggings.objects.filter(question=Questions.objects.get(pk=q6_id),
                                            tag=Tags.objects.get(name=t6_id)).delete()

            if form.is_valid():
                return redirect('list_questions')

        return render(request, 'questions-form.html',
                      {'form': form, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5, 'form6': form6})
