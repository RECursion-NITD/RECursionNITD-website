from django.contrib.auth.models import User
from user_profile.models import Profile
import os
import random
import urllib.request
from urllib.error import URLError, HTTPError
import mimetypes
from django.core.files.base import ContentFile
from django.conf import settings
from django.shortcuts import redirect

def associate_by_email(**kwargs):
    try:
        #import pdb;pdb.set_trace();
        email = kwargs['details']['email']
        print(email)
        kwargs['user'] = User.objects.get(email=email)
        print(kwargs['user'])
    except:
        print("error")
        pass
    return kwargs

def _save_image_from_url_to_profile(user, image_url):
    """
    Download image_url and save into user.profile.image using Django storage.
    Returns True on success, False on failure. Saves to 'images/<username>.<ext>'.
    """
    try:
        # Request with a common User-Agent to avoid blocking by some servers
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            # try to get content-type to derive extension
            content_type = resp.info().get_content_type()
        ext = mimetypes.guess_extension(content_type) or '.png'
        filename = f"images/{user.username}{ext}"
        # Save using Django File storage so ImageField works as expected
        user.profile.image.save(filename, ContentFile(data), save=True)
        return True
    except (HTTPError, URLError, ValueError, Exception) as e:
        # print full exception so you can diagnose (network, ssl, 403, etc.)
        print("profile image download failed:", repr(e))
        return False

def set_image_for_new_users(backend, user, response, *args, **kwargs):
    #import pdb;pdb.set_trace();
    try:
        if not user.profile.email_confirmed:
            user.profile.email_confirmed=True
            user.save()

        if not user.profile.name:
            try:
                user.profile.name = response.get('name')
            except:
                user.profile.name = user.username    
            user.profile.college = "none"
            user.save()
                        
        if not user.profile.image:
            # try provider picture first
            try:
                image_url = response.get('picture')
                if image_url:
                    ok = _save_image_from_url_to_profile(user, image_url)
                    if ok:
                        return
                # fallback to site default
                image_url = 'https://recursionnitd.in/static/image/profile_pic/' + str(random.randint(1,15)) + '.png'
                ok = _save_image_from_url_to_profile(user, image_url)
                if not ok:
                    print("Downloadable Image Not Found!")
            except Exception as e:
                print("set_image_for_new_users error:", repr(e))
                print("Downloadable Image Not Found!")
    except Exception as e:
        print("set_image_for_new_users outer error:", repr(e))
        pass