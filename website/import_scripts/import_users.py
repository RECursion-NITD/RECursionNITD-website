#import python's built-in csv library
from django.contrib.auth.models import User
from user_profile.models import Profile
import urllib.request
import random
import csv
from random import choice
from string import ascii_uppercase
from website.utils import save_local_profile_pic_to_media


randhash = ''.join(choice(ascii_uppercase) for i in range(32))

# open the file in read mode
with open('import_scripts/user.csv', 'r') as csvfile:

    # convert the data in this file into a DictReader
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['Name'])
        username = row['Name'].replace(' ','_')
        c=1
        if User.objects.filter(username__iexact=username).exists():
            username=username+str(c)
            while User.objects.filter(username__iexact=username).exists():
                username = username[:-1]+str(c)
                c+=1
        u = User(username=username,password=randhash,email = row['Email'])
        u.save()
        #import pdb;pdb.set_trace()
        if row['Nickname'] == '-':
            u.profile.name = row['Name']
        else:
            u.profile.name = row['Nickname']
        
        u.profile.college = row['College']
        u.profile.dept = row['Dept']
        u.profile.email_confirmed=True
        #Development
        #For development
        # image_url = 'http://127.0.0.1:8000/'+'static/image/profile_pic/' + str(random.randint(1,15)) + '.png'
        #Production: copy local static into MEDIA instead of fetching external URL
        try:
            rel_media = save_local_profile_pic_to_media(username)
        except Exception as e:
            print("import_users: save_local_profile_pic_to_media exception:", repr(e))
            rel_media = False

        if not rel_media:
            print("Downloadable Image Not Found!")
        else:
            u.profile.image = rel_media  # relative to MEDIA_ROOT
        u.save()









