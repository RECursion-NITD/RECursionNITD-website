#import python's built-in csv library
from django.contrib.auth.models import User
from user_profile.models import Profile
import urllib.request
import random
import csv
from random import choice
from string import ascii_uppercase


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
        image_url = 'https://recursionnitd.in/'+'static/image/profile_pic/' + str(random.randint(1,15)) + '.png'
        full_path = 'media/images/' + username + '.png'
        try:
            urllib.request.urlretrieve(image_url, full_path)
        except:
            print("Downloadable Image Not Found!")
        u.profile.image = '../' + full_path
        u.save()
        
        

        





