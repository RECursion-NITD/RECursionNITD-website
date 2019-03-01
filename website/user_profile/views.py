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


def view_profile(request, id):
    try:
        user = get_object_or_404(User, pk=id)
    except:
        print(request.user.id)
        return HttpResponse("User does not exist!")
    try:
        profile = get_object_or_404(Profile, user=user)
    except:
        return HttpResponse("User has not created a Profile yet!")

    args = {'profile': profile, }
    return render(request, 'profile/profile.html', args)


def user_register(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST':
      if request.POST.get('ajax_check') == "True":
          if form.is_valid():
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
          form = EmailForm(None)
          return HttpResponse('Invalid Credentials!')
    return render(request, 'register.html', {'form': form})


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
        return redirect('edit_profile')
    else:
        return render(request, 'account_activation_invalid.html')


@login_required
def edit_profile(request):
    form = Profileform(request.POST or None)
    user = request.user
    id = user.id
    profile = get_object_or_404(Profile, user=user)
    form = Profileform(request.POST or None, instance=profile)
    if request.POST.get('ajax_check') == "True":
      if form.is_valid():
          image_url = form.cleaned_data['image_url']
          type = valid_url_extension(image_url)
          full_path = 'media/images/' + profile.user.username + '.png'
          try:
              urllib.request.urlretrieve(image_url, full_path)
          except:
              return HttpResponse("Downloadable Image Not Found!")
          if profile.user == request.user:
              profile.image = '../' + full_path
              form.save()
              return HttpResponse('Information Updated Successfully!')
      form = Profileform(None)
      return HttpResponse('Invalid Credentials!')
    return render(request, 'create.html', {'form': form, })


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST':
        if request.POST.get('ajax_check') == "True":
          if form.is_valid():
              user = form.save()
              update_session_auth_hash(request, user)  # Important!
              messages.success(request, 'Your password was successfully updated!')
              return HttpResponse("Password Changed Successfully!")
          else:
              messages.error(request, 'Please correct the Error below.')
          form = PasswordChangeForm(request.user)
          return HttpResponse('Invalid Credentials!')
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def password_reset(request):
    form = EmailForm(request.POST or None)
    if request.method == 'POST':
        if request.POST.get('ajax_check') == "True":
          if form.is_valid():
              email = form.cleaned_data['email']
              if (User.objects.filter(email=email).count() > 1):
                  return HttpResponse("Email Already Used!")
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