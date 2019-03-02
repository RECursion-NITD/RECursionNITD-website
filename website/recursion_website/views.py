from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
from user_profile.models import Profile
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
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .tokens import password_reset_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import send_mass_mail

@login_required
def home(request):
    return render(request, 'home.html')

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
        description = form.cleaned_data.get('description')
        if description.__len__() < 10:
            return HttpResponse("Very Short Question's Description!")
        f = form.save(commit=False)
        f.user_id = request.user
        form.save()
    if form2.is_valid():
        f2 = form2.save(commit=False)
        tagging_list = []
        q_id = f.id
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
        profiles=Profile.objects.filter(role = 2)
        messages=()
        for profile in profiles:
           user = profile.user
           current_site = get_current_site(request)
           subject = 'New Activity in AskREC'
           message = render_to_string('new_question_entry_email.html', {
              'user': user,
              'domain': current_site.domain,
              'question' : Questions.objects.get(pk=f.id),
           })
           msg=(subject, message, 'webmaster@localhost', [user.email])
           messages += (msg,)
        result = send_mass_mail(messages, fail_silently=False)
        return redirect('list_questions')

    return render(request, 'recursion_website/questions-form.html', {'form': form,'form2':form2,})

def list_questions(request):
    questions = Questions.objects.all()
    q_count=questions.count()
    answers=Answers.objects.all()
    follows=Follows.objects.all()
    taggings_recent = Taggings.objects.all().order_by('-updated_at')
    tags_recent=Tags.objects.all().order_by('-updated_at')
    tags_popular=[]
    if tags_recent.count()>10:
        limit=10
    else:
        limit=tags_recent.count()
    for tag in tags_recent:
        tagging = Taggings.objects.filter(tag=tag)
        count=tagging.count()
        tags_popular.append([count,tag])
    tags_popular.sort(key=lambda x: x[0],reverse=True)
    tags_recent_record=[]
    tags_popular_record=[]
    for i in range(limit):
        tags_popular_record.append(tags_popular[i][1])
    count=0
    while len(tags_recent_record)!= limit:
        if taggings_recent[count].tag not in tags_recent_record:
           tags_recent_record.append(taggings_recent[count].tag)
        count+=1

    args = {'questions':questions, 'answers':answers, 'follows':follows, 'tags':tags_recent, 'taggings':taggings_recent, 'tags_recent':tags_recent_record, 'tags_popular':tags_popular_record, 'q_count':q_count}
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
    comments_answers=Comments_Answers.objects.all()
    if User.objects.filter(username=request.user).exists():
        ans = Answers.objects.filter(user_id=request.user).filter(question_id=questions)
        if ans.count() > 0:
            ans = ans[0]
        else:
            ans = None
    else:
        ans=None
    user = request.user
    flag=0
    id_list = []
    if User.objects.filter(username=request.user).exists():
        if Follows.objects.filter(question=questions, user=user).exists():
            flag = 1
        votes = Upvotes.objects.filter(user=user).values("answer_id")
        id_list = [id['answer_id'] for id in votes]  # voted answers id

    args = {'questions': questions, 'answers': answers, 'follows': follows, 'tags':tags, 'taggings':taggings, 'upvotes':upvotes, 'comments':comments,'comments_answers':comments_answers,'ans':ans,'flag':flag,'voted':id_list, }
    return render(request, 'recursion_website/detail.html', args)

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
            description = form.cleaned_data.get('description')
            if description.__len__() < 10:
                return HttpResponse("Very Short Question's Description!")
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
            profiles = Profile.objects.filter(role=2)
            follows = Follows.objects.filter(question=question)
            messages = ()
            for profile in profiles:
                user = profile.user
                current_site = get_current_site(request)
                subject = 'New Activity in AskREC'
                message = render_to_string('update_question_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'question': question,
                })
                msg = (subject, message, 'webmaster@localhost', [user.email])
                messages += (msg,)
            for follow in follows:
                user = follow.user
                current_site = get_current_site(request)
                subject = 'New Activity in AskREC'
                message = render_to_string('update_question_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'question': question,
                })
                msg = (subject, message, 'webmaster@localhost', [user.email])
                if msg not in messages:
                    messages += (msg,)
            result = send_mass_mail(messages, fail_silently=False)
            return redirect('list_questions')
    else:
        question = Questions.objects.get(pk=id)
        id_list = Taggings.objects.filter(question=question).values('tag_id')  # get all tag ids from taggings
        id_list = [id['tag_id'] for id in id_list]  # convert the returned dictionary list into a simple list
        form2 = Tagform(queryset=Tags.objects.filter(id__in=id_list))  # populate form with tags

        return render(request, 'recursion_website/questions-form.html', {'form': form, 'form2': form2, 'question': question})

@login_required
def add_answer(request, id):

    try:
        question = get_object_or_404(Questions, pk=id)

    except:
        return HttpResponse("id does not exist")
    ans=Answers.objects.filter(user_id=request.user).filter(question_id=question)
    if ans.count()>0:
        return HttpResponse("you have already answered,kindly update it instead")
    form = Answerform(request.POST or None)
    if form.is_valid():
            description = form.cleaned_data.get('description')
            if description.__len__() < 10:
                return HttpResponse("Very Short Answer!")
            f = form.save(commit=False)
            f.question_id=question
            f.user_id = request.user
            form.save()
            profiles = Profile.objects.filter(role=2)
            follows=Follows.objects.filter(question=question)
            messages = ()
            for profile in profiles:
                user = profile.user
                current_site = get_current_site(request)
                subject = 'New Activity in AskREC'
                message = render_to_string('new_answer_entry_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'question': question,
                })
                msg = (subject, message, 'webmaster@localhost', [user.email])
                messages += (msg,)
            for follow in follows:
                user = follow.user
                current_site = get_current_site(request)
                subject = 'New Activity in AskREC'
                message = render_to_string('new_answer_entry_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'question': question,
                })
                msg = (subject, message, 'webmaster@localhost', [user.email])
                if msg not in messages:
                    messages += (msg,)
            result = send_mass_mail(messages, fail_silently=False)
            return HttpResponseRedirect(reverse('detail_questions', args=(question.id,)))

    ans=Answers.objects.filter(user_id=request.user).filter(question_id=question)

    return render(request, 'recursion_website/answer.html', {'form': form,'ans':ans})

@login_required
def update_answer(request, id):
    try:
        answer =get_object_or_404(Answers, pk=id)
        question=answer.question_id
    except:
        return HttpResponse("id does not exist")
    else:
        form = Answerform(request.POST or None, instance=answer)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            if description.__len__() < 10:
                return HttpResponse("Very Short Answer!")
            if request.user == answer.user_id:
              form.save()
              profiles = Profile.objects.filter(role=2)
              follows=Follows.objects.filter(question=question)
              messages = ()
              for profile in profiles:
                  user = profile.user
                  current_site = get_current_site(request)
                  subject = 'New Activity in AskREC'
                  message = render_to_string('answer_update_email.html', {
                      'user': user,
                      'domain': current_site.domain,
                      'question': question,
                  })
                  msg = (subject, message, 'webmaster@localhost', [user.email])
                  messages += (msg,)
              for follow in follows:
                  user = follow.user
                  current_site = get_current_site(request)
                  subject = 'New Activity in AskREC'
                  message = render_to_string('answer_update_email.html', {
                      'user': user,
                      'domain': current_site.domain,
                      'question': question,
                  })
                  msg = (subject, message, 'webmaster@localhost', [user.email])
                  if msg not in messages:
                     messages += (msg,)
              result = send_mass_mail(messages, fail_silently=False)
            return HttpResponseRedirect(reverse('detail_questions', args=(question.id,)))

    return render(request, 'recursion_website/answer.html', {'form': form, 'ans': answer})

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
    return HttpResponseRedirect(reverse('detail_questions', args=(question.id,)))

@login_required
def add_comment(request, id):
    try:
        question = get_object_or_404(Questions, pk=id)
    except:
        return HttpResponse("id does not exist")
    form = Commentform(request.POST or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.question=question
        f.user = request.user
        form.save()
        profiles = Profile.objects.filter(role=2)
        follows=Follows.objects.filter(question=question)
        messages = ()
        for profile in profiles:
            user = profile.user
            current_site = get_current_site(request)
            subject = 'New Activity in AskREC'
            message = render_to_string('new_comment_entry_email.html', {
                'user': user,
                'domain': current_site.domain,
                'question': question,
            })
            msg = (subject, message, 'webmaster@localhost', [user.email])
            messages += (msg,)
        for follow in follows:
            user = follow.user
            current_site = get_current_site(request)
            subject = 'New Activity in AskREC'
            message = render_to_string('new_comment_entry_email.html', {
                'user': user,
                'domain': current_site.domain,
                'question': question,
            })
            msg = (subject, message, 'webmaster@localhost', [user.email])
            if msg not in messages:
                messages += (msg,)
        result = send_mass_mail(messages, fail_silently=False)
        return HttpResponseRedirect(reverse('detail_questions', args=(question.id,)))

    return render(request, 'recursion_website/comment.html', {'form': form})

@login_required
def update_comment(request, id):
    try:
        comment =get_object_or_404(Comments, pk=id)
        question=comment.question
    except:
        return HttpResponse("id does not exist")
    else:
        form = Commentform(request.POST or None, instance=comment)
        if form.is_valid():
            if request.user == comment.user:
              form.save()
              profiles = Profile.objects.filter(role=2)
              follows=Follows.objects.filter(question=question)
              messages = ()
              for profile in profiles:
                  user = profile.user
                  current_site = get_current_site(request)
                  subject = 'New Activity in AskREC'
                  message = render_to_string('update_comment_email.html', {
                      'user': user,
                      'domain': current_site.domain,
                      'question': question,
                  })
                  msg = (subject, message, 'webmaster@localhost', [user.email])
                  messages += (msg,)
              for follow in follows:
                  user = follow.user
                  current_site = get_current_site(request)
                  subject = 'New Activity in AskREC'
                  message = render_to_string('update_comment_email.html', {
                      'user': user,
                      'domain': current_site.domain,
                      'question': question,
                  })
                  msg = (subject, message, 'webmaster@localhost', [user.email])
                  if msg not in messages:
                     messages += (msg,)
              result = send_mass_mail(messages, fail_silently=False)
            return HttpResponseRedirect(reverse('detail_questions', args=(question.id,)))

    return render(request, 'recursion_website/comment.html', {'form': form, 'comment': comment})

@login_required
def voting(request, id):
    try:
        answer =get_object_or_404( Answers,pk=id)
        question=answer.question_id
    except:
        return HttpResponse("id does not exist")
    user = request.user
    if user != answer.user_id:
       if Upvotes.objects.filter(answer=answer, user=user).exists():
           upvote= Upvotes.objects.get(answer=answer, user=user)
           upvote.delete()
       else:
           upvote = Upvotes.objects.create(answer=answer, user=user)
           upvote.save()
    return HttpResponseRedirect(reverse('detail_questions', args=(question.id,)))



def filter_question(request ,id):
    try:
        required_tag=get_object_or_404(Tags, pk=id)
    except:
        return HttpResponse("Tag does not exist!")
    questions=[]
    answers=Answers.objects.all()
    follows=Follows.objects.all()
    taggings=Taggings.objects.filter(tag=required_tag)
    for tagging in taggings:
        questions.append(tagging.question)
    tags_recent=Tags.objects.all().order_by('-updated_at')
    taggings_recent=Taggings.objects.all().order_by('-updated_at')
    tags_popular = []
    if tags_recent.count() > 10:
        limit = 10
    else:
        limit = tags_recent.count()
    for tag in tags_recent:
        tagging = Taggings.objects.filter(tag=tag)
        count = tagging.count()
        tags_popular.append([count, tag])
    tags_popular.sort(key=lambda x: x[0], reverse=True)
    tags_recent_record = []
    tags_popular_record = []
    for i in range(limit):
        tags_popular_record.append(tags_popular[i][1])
    count=0
    while len(tags_recent_record)!= limit:
        if taggings_recent[count].tag not in tags_recent_record:
           tags_recent_record.append(taggings_recent[count].tag)
        count+=1
    questions.reverse()
    q_count=Questions.objects.all().count()
    args = {'questions':questions, 'answers':answers, 'follows':follows, 'tags':tags_recent, 'taggings':taggings_recent, 'tags_recent':tags_recent_record, 'tags_popular':tags_popular_record, 'q_count':q_count}
    return render(request, 'questions.html', args)


@login_required
def add_comment_answer(request, id):
    try:
        answer = get_object_or_404(Answers, pk=id)
    except:
        return HttpResponse("id does not exist")
    form = Comment_Answerform(request.POST or None)
    if form.is_valid():
        question_id=answer.question_id
        f = form.save(commit=False)
        f.answer=answer
        f.user = request.user
        form.save()
        profiles = Profile.objects.filter(role=2)
        follows=Follows.objects.filter(question=question_id)
        messages = ()
        for profile in profiles:
            user = profile.user
            current_site = get_current_site(request)
            subject = 'New Activity in AskREC'
            message = render_to_string('new_answer_comment_entry_email.html', {
                'user': user,
                'domain': current_site.domain,
                'question': answer.question_id,
            })
            msg = (subject, message, 'webmaster@localhost', [user.email])
            messages += (msg,)
        for follow in follows:
            user = follow.user
            current_site = get_current_site(request)
            subject = 'New Activity in AskREC'
            message = render_to_string('new_answer_comment_entry_email.html', {
                'user': user,
                'domain': current_site.domain,
                'question': answer.question_id,
            })
            msg = (subject, message, 'webmaster@localhost', [user.email])
            if msg not in messages:
                messages += (msg,)
        result = send_mass_mail(messages, fail_silently=False)
        return HttpResponseRedirect(reverse('detail_questions', args=(question_id.id,)))

    return render(request, 'recursion_website/comment.html', {'form': form})

@login_required
def update_comment_answer(request, id):
    try:
        comment =get_object_or_404(Comments_Answers, pk=id)
        answer=comment.answer
    except:
        return HttpResponse("id does not exist")
    else:
        question_id=answer.question_id
        form = Comment_Answerform(request.POST or None, instance=comment)
        if form.is_valid():
            if request.user == comment.user:
              form.save()
              profiles = Profile.objects.filter(role=2)
              follows=Follows.objects.filter(question=question_id)
              messages = ()
              for profile in profiles:
                  user = profile.user
                  current_site = get_current_site(request)
                  subject = 'New Activity in AskREC'
                  message = render_to_string('update_answer_comment_email.html', {
                      'user': user,
                      'domain': current_site.domain,
                      'question': answer.question_id,
                  })
                  msg = (subject, message, 'webmaster@localhost', [user.email])
                  messages += (msg,)
              for follow in follows:
                  user = follow.user
                  current_site = get_current_site(request)
                  subject = 'New Activity in AskREC'
                  message = render_to_string('update_answer_comment_email.html', {
                      'user': user,
                      'domain': current_site.domain,
                      'question': answer.question_id,
                  })
                  msg = (subject, message, 'webmaster@localhost', [user.email])
                  if msg not in messages:
                     messages += (msg,)
              result = send_mass_mail(messages, fail_silently=False)
            return HttpResponseRedirect(reverse('detail_questions', args=(question_id.id,)))

    return render(request, 'recursion_website/comment.html', {'form': form, 'comment': comment})

