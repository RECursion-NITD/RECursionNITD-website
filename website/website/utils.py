from django.contrib.auth.models import User
from user_profile.models import Profile
import urllib.request
import random
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

def set_image_for_new_users(backend, user, response, *args, **kwargs):
    import pdb;pdb.set_trace();
    try:
        if not user.profile.email_confirmed:
            user.profile.email_confirmed=True
            user.save()
        if not user.profile.image:
            p = Profile.objects.get(user=user)
            print(p)
            p.name = user.username
            p.college = "none"
            image_url = "https://api.adorable.io/avatars/"+ str(random.randint(0000,9999))
            full_path = 'media/images/' + user.username + '.png'
            try:
                urllib.request.urlretrieve(image_url, full_path)
                p.image = '../' + full_path
                p.save()
            except:
                print("Downloadable Image Not Found!")
            
        
    except:
        print("error")
        pass

 
