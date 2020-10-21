from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
from user_profile.models import *
from events.models import *
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
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import send_mass_mail
import json
import datetime
import html2markdown
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from difflib import SequenceMatcher
from django.utils import timezone
from datetime import timedelta

json.JSONEncoder.default = lambda self,obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)

def tagging_add(q_id, t_id):
    p = Taggings.objects.create(question=get_object_or_404(Posts, pk=q_id), tag=get_object_or_404(Tags, pk=t_id))
    return

def bulk_tagging_add(question, tags):
    taggings = []
    for tag in tags:
        taggings.append(Taggings(post=post, tag=tag))
    Taggings.objects.bulk_create(taggings)
    return

@login_required
def add_blog(request):
    form = Postform(request.POST or None)

    Tagform = modelformset_factory(Tags, fields=('name',), extra=5)
    if request.method=='POST':
        form2 = Tagform(request.POST)
        if form.is_valid() and form2.is_valid():
            f = form.save(commit=False)
            f.user_id = request.user
            form.save()
            f2 = form2.save(commit=False)
            tagging_list = []
            p_id = f.id
            for item in f2:
                if Tags.objects.filter(name=item.name).exists():
                    tag = Tags.objects.get(name=item.name)
                else:
                    item.save()
                    tag=item
                if tag not in tagging_list:
                    tagging_list.append(tag)

            bulk_tagging_add(f, tagging_list)  # use a bulk create function which accepts a list
            profiles=Profile.objects.filter(role = 2)
            messages=()
            for profile in profiles:
                user = profile.user
                current_site = get_current_site(request)
                subject = 'New Activity in AskREC'
                message = render_to_string('new_question_entry_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'post' : Posts.objects.get(pk=f.id),
                })
                msg=(subject, message, 'webmaster@localhost', [user.email])
                messages += (msg,)
                result = send_mass_mail(messages, fail_silently=False)
            return redirect('list_blogs')

    else:
         form2 = Tagform(queryset=Tags.objects.none())

    return render(request, 'blog/blog_form.html', {'form': form,'form2':form2,})


def list_blogs(request):
    search = SearchForm(request.POST or None)
    if request.method == 'POST':
        if search.is_valid():
          key_req = search.cleaned_data
          key = key_req.get('key')
          return HttpResponseRedirect(reverse('search_blog', args=(key,)))
    posts = Posts.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts_list = paginator.page(paginator.num_pages)
    p_count=posts.count()
    reply=Reply.objects.all()
    taggings_recent = Taggings.objects.all().order_by('-updated_at')
    tags_recent=Tags.objects.all().order_by('-updated_at')
    tags_popular=[]
    check = []
    if tags_recent.count()>10:
        limit=10
    else:
        limit=tags_recent.count()
    for tag in tags_recent:
        tagging = Taggings.objects.filter(tag=tag)
        count=tagging.count()
        tags_popular.append([count,tag])
        if count>0:
            check.append(tag)
    tags_popular.sort(key=lambda x: x[0],reverse=True)
    tags_recent_record=[]
    tags_popular_record=[]
    for i in range(limit):
        tags_popular_record.append(tags_popular[i][1])
    count=0
    # import pdb;pdb.set_trace();
    while len(tags_recent_record)< len(taggings_recent) and len(tags_recent_record)< len(check) and len(tags_recent_record) < 10:
        if taggings_recent[count].tag not in tags_recent_record:
           tags_recent_record.append(taggings_recent[count].tag)
        count+=1
    profiles=Profile.objects.all()
    args = {'form_search':search,'profile':profiles, 'posts':posts_list, 'reply':reply, 'tags':tags_recent, 'taggings':taggings_recent, 'tags_recent':tags_recent_record, 'tags_popular':tags_popular_record, 'p_count':p_count}
    if request.is_ajax():
        return render(request, 'blog/blog_list.html', args)
    return render(request, 'blog/blog_homepage.html', args)


def detail_blogs(request, id):
    comform = Commentform(request.POST or None)
    repform = Replyform(request.POST or None)

    try:
        posts =get_object_or_404( Posts,pk=id)
    except:
        return HttpResponse("id does not exist")
    reply = Reply.objects.filter(post_id = posts)
    tags = Tags.objects.all()
    taggings = Taggings.objects.all()
    likes=Likes.objects.all()
    comment=Comment.objects.filter(post = posts)
    comment_reply=Comment_Reply.objects.all()
    profile=Profile.objects.all()
    if User.objects.filter(username=request.user).exists():
        rep = Reply.objects.filter(user_id=request.user).filter(post_id=posts)
        if rep.count() > 0:
            rep = rep[0]
        else:
            rep = None
    else:
        rep=None
    if request.user.is_authenticated:
        user = request.user
        user_profile = Profile.objects.get(user=user)
        user_permission = user_profile.role
    else:
        user_permission = '10'
    flag=0
    id_list = []
    if User.objects.filter(username=request.user).exists(): 
        votes = Likes.objects.filter(user=user).values("reply_id")
        id_list = [id['reply_id'] for id in votes]  # voted answers id


    args = {'profile':profile,'user_permission':user_permission,'comform':comform,'repform':repform,'posts': posts, 'reply':reply, 'tags':tags, 'taggings':taggings, 'likes':likes, 'comment':comment,'comment_reply':comment_reply,'rep':rep,'flag':flag}
    return render(request, 'blog/blog_details.html', args) 

@login_required
def update_blogs(request, id):
    try:
        post = get_object_or_404(Posts, pk=id)
    except:
        return HttpResponse("id does not exist")
    # import pdb;pdb.set_trace();
    form = Postform(request.POST or None, instance=post)
    Tagform = modelformset_factory(Tags, fields=('name',), extra=1)
    if request.method == 'POST':
        form2 = Tagform(request.POST or None)
        if form.is_valid() and  form2.is_valid():
            description = form.cleaned_data.get('description')
            f = form.save(commit=False)
            f.user_id = request.user
            form.save()
            to_del = Taggings.objects.filter(post=post)  # delete all prev taggings
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

            bulk_tagging_add(post, tagging_list)  # use a bulk create function which accepts a list
            profiles = Profile.objects.filter(role=2)
            messages = ()
            for profile in profiles:
                user = profile.user
                current_site = get_current_site(request)
                subject = 'New Activity in AskREC'
                message = render_to_string('update_question_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'post': post,
                })
                msg = (subject, message, 'webmaster@localhost', [user.email])
                messages += (msg,)
            '''for follow in follows:
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
                    messages += (msg,)'''
            result = send_mass_mail(messages, fail_silently=False)
            return redirect('list_blogs')
    else:
        import html2text
        h = html2text.HTML2Text()
        post.description = h.handle(post.description)
        form = Postform(instance=post)
        post = Posts.objects.get(pk=id)
        id_list = Taggings.objects.filter(post=post).values('tag_id')  # get all tag ids from taggings
        id_list = [id['tag_id'] for id in id_list]  # convert the returned dictionary list into a simple list
        form2 = Tagform(queryset=Tags.objects.filter(id__in=id_list))  # populate form with tags

    return render(request, 'blog/blog_form.html', {'form': form, 'form2': form2, 'post': post})

@login_required
def add_reply(request, id):

    try:
        post = get_object_or_404(Posts, pk=id)

    except:
        return HttpResponse("id does not exist")

    rep=Reply.objects.filter(user_id=request.user).filter(post_id=post)
    if rep.count()>0:
        return HttpResponse("you have already answered,kindly update it instead")
    form = Replyform(request.POST or None)
    if request.POST.get('ajax_call') == "True" :
        if form.is_valid():
            description = form.cleaned_data.get('description')
            print(description)
            if len(description) < 10:
                return HttpResponse("Very Short Answer!")
            f = form.save(commit=False)
            f.post_id=post
            f.user_id = request.user
            form.save()
            profiles = Profile.objects.filter(role=2) # only role 2 profile
            comment_reply=Comment_Reply.objects.all()
            prof=Profile.objects.all()  # all user profile
            replys=Reply.objects.filter(post_id=post)
            messages = ()
            for profile in profiles:
                user = profile.user
                current_site = get_current_site(request)
                subject = 'New Activity in AskREC'
                message = render_to_string('new_answer_entry_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'post': post,
                })
                msg = (subject, message, 'webmaster@localhost', [user.email])
                messages += (msg,)
            '''for follow in follows:
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
                    messages += (msg,)'''
            result = send_mass_mail(messages, fail_silently=False)
            user= request.user
            f_p_id=Posts.objects.get(pk=id)
            f.post_id=f_p_id
            f.user_id =user
            f.save()

            args = {'profile':prof,'replys': replys,  'comment_reply':comment_reply,'post':post}
            return render(request, 'blog/div_reply.html',args)
        else :
            return HttpResponse("we failed to insert in db")
    else:
        return render(request, 'blog/reply.html', {'form': form})

@login_required
def update_reply(request, id):
    try:
        reply =get_object_or_404(Reply, pk=id)
        post=reply.post_id
    except:
        return HttpResponse("id does not exist")
    else:
        form = Replyform(request.POST or None, instance=reply)
        if request.method == 'POST':
            if form.is_valid():
                description = form.cleaned_data.get('description')
                if description.__len__() < 10:
                    return HttpResponse("Very Short Answer!")
                user = request.user
                user_profile = Profile.objects.get(user=user)
                user_permission = user_profile.role
                comment_reply=Comment_Reply.objects.all()
                prof=Profile.objects.all()  # all user profile
                replys=Reply.objects.filter(post_id=post)
                if request.user == reply.user_id or user_permission == '2' or user_permission == '1':
                    f=form.save()
                    profiles = Profile.objects.filter(role=2)
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
                    '''for follow in follows:
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
                            messages += (msg,)'''
                    result = send_mass_mail(messages, fail_silently=False)
                    args = {'profile':prof,'replys': replys,  'comment_reply':comment_reply,'post':post }
                    return render(request, 'blog/div_reply.html',args)

        import html2text
        h = html2text.HTML2Text()
        reply.description = h.handle(reply.description)
        form=Replyform(instance=reply)


    return render(request, 'blog/reply.html', {'upform': form, 'rep': reply})

@login_required
def add_comment(request, id):
    try:
        post = get_object_or_404(Posts, pk=id)
    except:
        return HttpResponse("id does not exist")
    form = Commentform(request.POST or None)
    if form.is_valid():
        f = form.save(commit=False)
        f.post=post
        f.user = request.user
        form.save()
        profiles = Profile.objects.filter(role=2) #only  role 2 profile
        prof=Profile.objects.all()  #all user profile
        messages = ()
        for profile in profiles:
            user = profile.user
            current_site = get_current_site(request)
            subject = 'New Activity in AskREC'
            message = render_to_string('new_comment_entry_email.html', {
                'user': user,
                'domain': current_site.domain,
                'post': post,
            })
            msg = (subject, message, 'webmaster@localhost', [user.email])
            messages += (msg,)
        '''for follow in follows:
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
                messages += (msg,)'''
        result = send_mass_mail(messages, fail_silently=False)
        user= request.user
        comment=Comment.objects.filter(post = post)
        args = {'profile':prof,'post': post,  'comment':comment, }
        return render(request, 'blog/div_comment.html',args)
    else:
        return  HttpResponse("Invalid")

    return render(request, 'blog/comment.html', {'form':form})

@login_required
def update_comment(request, id):
    print(id)
    try:
        comment =get_object_or_404(Comment, pk=id)
        post=comment.post
    except:
        return HttpResponse("id does not exist")
    else:
        if request.method == 'POST':
            form = Commentform(request.POST or None, instance=comment)
            if form.is_valid():
                user = request.user
                user_profile = Profile.objects.get(user=user)
                user_permission = user_profile.role
                if request.user == comment.user or user_permission == '2' or user_permission == '1':
                    f=form.save()
                    profiles = Profile.objects.filter(role=2)
                    messages = ()
                    for profile in profiles:
                        user = profile.user
                        current_site = get_current_site(request)
                        subject = 'New Activity in AskREC'
                        message = render_to_string('update_comment_email.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'post': post,
                        })
                        msg = (subject, message, 'webmaster@localhost', [user.email])
                        messages += (msg,)
                    '''for follow in follows:
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
                            messages += (msg,)'''
                    result = send_mass_mail(messages, fail_silently=False)
                    comment=Comment.objects.filter(post = post)
                    prof=Profile.objects.all()  #all user profile
                    args = {'profile':prof,'post': post,  'comment':comment}
                    return render(request, 'blog/div_comment.html',args)

        import html2text
        h = html2text.HTML2Text()
        comment.body = h.handle(comment.body)
        form=Commentform(instance=comment)
    return render(request, 'blog/comment.html', {'upform': form, 'comment': comment})

@login_required
def votings(request, id):
    try:
        reply =get_object_or_404( Reply,pk=id)
        reply=reply.question_id
    except:
        return HttpResponse("id does not exist")
    user = request.user
    count=0
    if user != reply.user_id:
       if Likes.objects.filter(reply=reply, user=user).exists():
           like= Likes.objects.get(reply=reply,user=user)
           like.delete()
           if Likes.objects.filter(reply=reply).exists():
               count=Likes.objects.filter(reply=reply).count()
           return HttpResponse(json.dumps({
                        'count':count,
                        'Success':'downvoted'
                            }))
       else:
           like = Likes.objects.create(reply=Reply, user=user)
           like.save()
           if Likes.objects.filter(reply=reply).exists():
               count=Likes.objects.filter(reply=reply).count()
           return HttpResponse(json.dumps({
                        'count':count,
                        'Success':'upvoted'
                            }))
    




def filter_blog(request ,id):
    search = SearchForm(request.POST or None)
    if request.method == 'POST':
        if search.is_valid():
            key_req = search.cleaned_data
            key = key_req.get('key')
            return HttpResponseRedirect(reverse('search_post', args=(key,)))
    try:
        required_tag=get_object_or_404(Tags, pk=id)
    except:
        return HttpResponse("Tag does not exist!")
    posts=[]
    reply=Reply.objects.all()
    taggings=Taggings.objects.filter(tag=required_tag)
    for tagging in taggings:
        posts.append(tagging.post)
    tags_recent=Tags.objects.all().order_by('-updated_at')
    taggings_recent=Taggings.objects.all().order_by('-updated_at')
    tags_popular = []
    check = []
    if tags_recent.count() > 10:
        limit = 10
    else:
        limit = tags_recent.count()
    for tag in tags_recent:
        tagging = Taggings.objects.filter(tag=tag)
        count = tagging.count()
        tags_popular.append([count, tag])
        if count>0:
            check.append(tag)
    tags_popular.sort(key=lambda x: x[0], reverse=True)
    tags_recent_record = []
    tags_popular_record = []
    for i in range(limit):
        tags_popular_record.append(tags_popular[i][1])
    count=0
    # import pdb;pdb.set_trace();
    while len(tags_recent_record) < len(taggings_recent) and len(tags_recent_record) < len(check) and len(tags_recent_record) < 10:
        if taggings_recent[count].tag not in tags_recent_record:
           tags_recent_record.append(taggings_recent[count].tag)
        count+=1
    p_count = Posts.objects.all().count() #For displaying total number of questions
    posts.reverse()
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts_list = paginator.page(paginator.num_pages)
    profiles = Profile.objects.all()
    args = {'form_search':search, 'profile': profiles, 'posts':posts_list, 'reply':reply, 'tags':tags_recent, 'taggings':taggings_recent, 'tags_recent':tags_recent_record, 'tags_popular':tags_popular_record, 'p_count':p_count}
    if request.is_ajax():
        return render(request, 'blog_list.html', args)
    return render(request, 'blog_homepage.html', args)

@login_required
def add_comment_reply(request, id):
    try:
        reply = get_object_or_404(Reply, pk=id)
    except:
        return HttpResponse("id does not exist")
    form = Comment_Replyform(request.POST or None)
    if form.is_valid():
        post_id=reply.post_id
        f = form.save(commit=False)
        f.reply=reply
        f.user = request.user
        form.save()
        profiles = Profile.objects.filter(role=2)
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
        '''for follow in follows:
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
                messages += (msg,)'''
        result = send_mass_mail(messages, fail_silently=False)
        prof=Profile.objects.all()
        replys=Reply.objects.filter(post_id=reply.post_id)
        comment_reply=Comment_Reply.objects.all()
        post=reply.post_id
        args = {'profile':prof,'replys': replys,  'comment_reply':comment_reply,'post':post}
        return render(request, 'fblog/div_reply.html',args)

    return render(request, 'blog/comment_a.html', {'upform': form})

@login_required
def update_comment_reply(request, id):
    try:
        comment =get_object_or_404(Comment_Reply, pk=id)
        reply=comment.reply
    except:
        return HttpResponse("id does not exist")
    else:
        post_id=reply.post_id
        form = Comment_Replyform(request.POST or None, instance=comment)
        if form.is_valid():
            user = request.user
            user_profile = Profile.objects.get(user=user)
            user_permission = user_profile.role
            if request.user == comment.user or user_permission == '2' or user_permission == '1':
              form.save()
              profiles = Profile.objects.filter(role=2)
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
              '''for follow in follows:
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
                     messages += (msg,)'''
              result = send_mass_mail(messages, fail_silently=False)
            prof=Profile.objects.all()
            replys=Reply.objects.filter(post_id=reply.post_id)
            comment_reply=Comment_Reply.objects.all()
            post=reply.post_id
            args = {'profile':prof,'replys': replys,  'comment_reply':comment_reply,'post':post }
            return render(request, 'blog/div_reply.html',args)
    import html2text
    h = html2text.HTML2Text()
    comment.body = h.handle(comment.body)
    form=Commentform(instance=comment)       

    return render(request, 'blog/comment_a.html', {'upform': form, 'comment': comment})


@login_required
def delete_reply(request, id):
    try:
        reply =get_object_or_404( Reply,pk=id)
        print(reply)
    except:
        return HttpResponse("id does not exist")
    user = request.user
    user_profile = Profile.objects.get(user=user)
    user_permission = user_profile.role
    post=reply.post_id
    if user_permission == '2' or user_permission == '1':
           reply.delete()
    return HttpResponseRedirect(reverse('detail_posts', args=(post.id,)))

@login_required
def delete_comment(request, id):
    try:
        comment =get_object_or_404( Comment,pk=id)
    except:
        return HttpResponse("id does not exist")
    user = request.user
    user_profile = Profile.objects.get(user=user)
    user_permission = user_profile.role
    post = comment.post
    if user_permission == '2' or user_permission == '1':
           comment.delete()
    return HttpResponseRedirect(reverse('detail_posts', args=(post.id,)))

@login_required
def delete_reply_comment(request, id):
    try:
        reply_comment =get_object_or_404(Comment_Reply,pk=id)
    except:
        return HttpResponse("id does not exist")
    user = request.user
    user_profile = Profile.objects.get(user=user)
    user_permission = user_profile.role
    post = reply_comment.reply.post_id
    if user_permission == '2' or user_permission == '1':
           reply_comment.delete()
    return HttpResponseRedirect(reverse('detail_posts', args=(post.id,)))


def search_blog(request, key):
     search = SearchForm(request.POST or None)
     if request.method == 'POST':
        if search.is_valid():
            key_req = search.cleaned_data
            key = key_req.get('key')
            return HttpResponseRedirect(reverse('search_blog', args=(key,)))
     posts_found=[]
     posts_list=Posts.objects.all()
     tags_found=[]
     tags_recent = Tags.objects.all().order_by('-updated_at')
     taggings_recent = Taggings.objects.all().order_by('-updated_at')
     for tag in tags_recent:
         if SequenceMatcher(None, tag.name.lower(), key.lower()).ratio()>0.4:
             tags_found.append(tag)
     for tag in tags_found:
         for tagging in taggings_recent:
             if tagging.tag==tag:
                 posts_found.append([SequenceMatcher(None, tag.name.lower(), key.lower()).ratio(), tagging.post])
     for post in posts_list:
         if SequenceMatcher(None, question.title.lower(), key.lower()).ratio()>0.3:
             posts_found.append([SequenceMatcher(None, post.title.lower(), key.lower()).ratio(), post])
     posts_found.sort(key=lambda x: x[0], reverse=True)
     posts=[]
     for post in posts_found:
         if post[1] not in posts:
            posts.append(post[1])
     reply = Reply.objects.all()
     tags_popular = []
     check = []
     if tags_recent.count() > 10:
         limit = 10
     else:
         limit = tags_recent.count()
     for tag in tags_recent:
         tagging = Taggings.objects.filter(tag=tag)
         count = tagging.count()
         tags_popular.append([count, tag])
         if count > 0:
             check.append(tag)
     tags_popular.sort(key=lambda x: x[0], reverse=True)
     tags_recent_record = []
     tags_popular_record = []
     for i in range(limit):
         tags_popular_record.append(tags_popular[i][1])
     count = 0
     while len(tags_recent_record) < len(taggings_recent) and len(tags_recent_record) < len(check) and len(tags_recent_record) < 10:
         if taggings_recent[count].tag not in tags_recent_record:
             tags_recent_record.append(taggings_recent[count].tag)
         count += 1
     p_count = Posts.objects.all().count()  # For displaying total number of questions
     paginator = Paginator(posts, 5)
     page = request.GET.get('page')
     try:
         posts_list = paginator.page(page)
     except PageNotAnInteger:
         posts_list = paginator.page(1)
     except EmptyPage:
         if request.is_ajax():
             return HttpResponse('')
         posts_list = paginator.page(paginator.num_pages)
     profiles = Profile.objects.all() 
     args = {'form_search':search, 'profile': profiles, 'posts': posts_list, 'posts': posts,
             'tags': tags_recent, 'taggings': taggings_recent, 'tags_recent': tags_recent_record,
             'tags_popular': tags_popular_record, 'p_count': p_count}
     if request.is_ajax():
         return render(request, 'blog/blog_list.html', args)
     return render(request, 'blog/blog_homepage.html', args) 

