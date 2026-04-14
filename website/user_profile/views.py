from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader, RequestContext
from django.template.loader import render_to_string
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.forms import modelformset_factory
from itertools import chain
from django.core.files.base import ContentFile
from io import BytesIO
import urllib.request
from PIL import Image
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token, password_reset_token
from django.contrib import messages
from .utils import ProfileMatcher, valid_url_extension
from website.utils import save_local_profile_pic_to_media
import random
from forum.models import *
from blog.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework_simplejwt.tokens import RefreshToken


def view_profile(request, id=None):
    if id == None:
        id = request.user.id
    try:
        user = get_object_or_404(User, pk=id) 
    except:
        print(request.user.id)
        return render(request,'id_error.html',{'no_user':1})
    try:
        profile = get_object_or_404(Profile, user=user)
    except:
        return render(request,'id_error.html',{'no_profile':1})
    posts = Posts.objects.filter(user_id = user).order_by('-updated_at')[:10:1]
    replys = Reply.objects.filter(user_id = user).order_by('-updated_at')[:10:1]
    comment = Comment.objects.filter(user = user).order_by('-updated_at')[:10:1]
    comment_rep= Comment_Reply.objects.filter(user = user).order_by('-updated_at')[:10:1]
    
    questions = Questions.objects.filter(user_id = user).order_by('-updated_at')[:10:1]
    answers = Answers.objects.filter(user_id = user).order_by('-updated_at')[:10:1]
    comments = Comments.objects.filter(user = user).order_by('-updated_at')[:10:1]
    comments_ans= Comments_Answers.objects.filter(user = user).order_by('-updated_at')[:10:1]

    required = []

    for question in questions:
        required.append(question)
    for answer in answers:
        required.append(answer)
    for comment_q in comments:
        required.append(comment_q)
    for com_a in comments_ans:
        required.append(com_a)
    
    for post in posts:  
        required.append(post)
    for reply in replys:
        required.append(reply)
    for com in comment:
        required.append(com)
    for com_r in comment_rep:
        required.append(com_r)

    required.sort(key=lambda x: x.updated_at, reverse=True)
    activity=[]
    k=0
    for req in required:
        activity.append(req)
        k+=1
        if k == 10:
            break

    args = {'profile': profile, 'activity':activity,}
    return render(request, 'profile/profile.html', args)


def user_register(request):
    if request.user.is_authenticated :
        id=request.user.id
        return HttpResponseRedirect(reverse('user_profile:view_profile', args=(id,)))
    form = SignUpForm(request.POST or None)
    if request.method == 'POST':
      if request.POST.get('ajax_check') == "True":
          if form.is_valid():
              if User.objects.filter(email=form.cleaned_data['email'].lower()).exists():
                  return HttpResponse("A user with that Email already exists.")
              user = form.save(commit=False)
              user.is_active = False
              user.save()
              current_site = get_current_site(request)
              subject = 'Activate Your RECursion Account'
              # ensure uid is a clean string (urlsafe_base64_encode returns str in recent Django)
              uid = urlsafe_base64_encode(force_bytes(user.pk))
              message = render_to_string('account_activation_email.html', {
                  'user': user,
                  'domain': current_site.domain,
                  'uid': uid,
                  'token': account_activation_token.make_token(user),
              })
              user.email_user(subject, message)
              return HttpResponse("Please confirm your email address to complete the Registration. ")
          if form.errors:
              for field in form:
                  for error in field.errors:
                      return HttpResponse(error)
          form = EmailForm(None)

    return render(request, 'register.html', {'form': form})


@login_required
def search_user(request):
    context={}
    query=request.GET.get('query','')
    matcher=ProfileMatcher(query=query)
    qs=Profile.objects.all()
    scored_matches=[(matcher.matcher(i),i) for i in qs if matcher.matcher(i)>=matcher.ratio_threshold]
    sorted_matches=sorted(scored_matches,key=lambda x: x[0],reverse=True)
    final_qs= list(map(lambda x:x[1],sorted_matches))
    # print(final_qs)
    context['tot']=len(final_qs)
    paginator = Paginator(final_qs, 20)
    page = request.GET.get('page')
    try:
        final_qs = paginator.page(page)
    except PageNotAnInteger:
        final_qs = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')

    context['matches']=final_qs
    if request.is_ajax():
        return render(request,'user_list.html',context=context)
    return render(request, 'user_search_res.html', context=context)


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        profile = Profile.objects.get(user = user)
        # Copy a local static profile pic into MEDIA and set ImageField
        try:
            rel_media = save_local_profile_pic_to_media(profile.user.username)
        except Exception as e:
            print("activate: save_local_profile_pic_to_media exception:", repr(e))
            rel_media = False

        if not rel_media:
            print("Downloadable Image Not Found!")
        else:
            profile.image.name = rel_media  # set path relative to MEDIA_ROOT
            profile.save()

        if profile.user == request.user:
            return redirect(settings.FRONTEND_BASE_URL + '/profile/edit?activated=true')
        return redirect(settings.FRONTEND_BASE_URL + '/profile/edit?activated=true')
    else:
        return render(request, 'account_activation_invalid.html')


@login_required
def edit_profile(request):
    user = request.user
    id = user.id
    profile = get_object_or_404(Profile, user=user)
    form = Profileform(request.POST or None, request.FILES or None,  instance=profile)
    if form.is_valid():
        form.save()
        # ensure a local default exists if no image supplied
        if not profile.image:
            try:
                rel_media = save_local_profile_pic_to_media(profile.user.username)
            except Exception as e:
                print("edit_profile: save_local_profile_pic_to_media exception:", repr(e))
                rel_media = False
            if rel_media:
                profile.image.name = rel_media
                profile.save()
        return HttpResponseRedirect(reverse('user_profile:view_profile', args=(id,)))
    return render(request, 'create.html', {'form': form, })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_profile:edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })

def password_reset(request):
    form = EmailForm(request.POST or None)
    if request.method == 'POST':
        if request.POST.get('ajax_check') == "True":
          if form.is_valid():
              email = form.cleaned_data['email']
              if not User.objects.filter(email=email).exists():
                  return HttpResponse("No user with that Email exists.")
              user = User.objects.get(email=email)
              user.save()
              current_site = get_current_site(request)
              subject = 'Reset Your RECursion Account Password'
              uid = urlsafe_base64_encode(force_bytes(user.pk))
              message = render_to_string('registration/password_reset_email.html', {
                  'user': user,
                  'domain': current_site.domain,
                  'uid': uid,
                  'token': password_reset_token.make_token(user),
                  'frontend_base_url': settings.FRONTEND_BASE_URL,
              })
              user.email_user(subject, message)
              return HttpResponse("We've emailed you instructions for setting your password, if an account exists with the email you entered! You should receive them shortly."
                                  "If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder.")
          form = EmailForm(None)
          return HttpResponse('Invalid')
    return render(request, 'registration/password_reset_form.html', {'form': form})


def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')


def password_reset_confirm(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


    # Use password_reset_token (was incorrectly using account_activation_token)
    if user is not None and password_reset_token.check_token(user, token):
        if request.method == 'POST':
            data = {
                'new_password1': request.POST.get('password'),
                'new_password2': request.POST.get('confirmPassword'),
            }
            form = SetPasswordForm(user, data=data)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                user.is_active = True
                user.save()
                return HttpResponse("Changed.")
            # if invalid, re-render with errors
            return HttpResponse(form)
        else:
            form = SetPasswordForm(user)
            return render(request, 'registration/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'registration/password_reset_invalid.html')


def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')

def username_check(request):
    username_typed=request.POST.get('username')
    if User.objects.filter(username = username_typed).exists():
        return HttpResponse("exists")
    return HttpResponse("success")

    
def email_check(request):
    email_typed=request.POST.get('email',"this email ID can't exist")
    email_typed=email_typed.lower()
    if User.objects.filter(email = email_typed).exists():
        return HttpResponse("exists")
    return HttpResponse("success")