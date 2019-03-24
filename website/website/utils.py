from django.contrib.auth.models import User

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