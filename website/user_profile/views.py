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
from django.contrib.auth.models import *
import random
from forum.models import *
from blog.models import *
from .utils import ProfileMatcher
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
              message = render_to_string('account_activation_email.html', {
                  'user': user,
                  'domain': current_site.domain,
                  'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
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
        image_url = 'https://recursionnitd.in/'+'static/image/profile_pic/' + str(random.randint(1,15)) + '.png'
        type = valid_url_extension(image_url)
        full_path = 'media/images/' + profile.user.username + '.png'
        try:
            urllib.request.urlretrieve(image_url, full_path)
        except:
            return HttpResponse("Downloadable Image Not Found!")
        if profile.user == request.user:
            profile.image = '../' + full_path
            profile.save()
        return redirect('user_profile:edit_profile')
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
        if form.cleaned_data['image'] is None or form.cleaned_data['image'] == False:
          image_url = 'https://recursionnitd.in/'+'static/image/profile_pic/' + str(random.randint(1,15)) + '.png'
          type = valid_url_extension(image_url)
          full_path = 'media/images/' + profile.user.username + '.png'
          try:
              urllib.request.urlretrieve(image_url, full_path)
          except:
              return HttpResponse("Downloadable Image Not Found!")
          if profile.user == request.user:
              profile.image = '../' + full_path
              form.save()
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
            return redirect('profile:edit_profile')
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
              message = render_to_string('registration/password_reset_email.html', {
                  'user': user,
                  'domain': current_site.domain,
                  'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                  'token': password_reset_token.make_token(user),
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

    if user is not None and account_activation_token.check_token(user, token):
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            user.is_active = True
            user.save()
            return redirect('login')
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