#import python's built-in csv library
from django.contrib.auth.models import User
from user_profile.models import Profile
import urllib.request
import random
import csv


randhash = "abcdef"
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
        p = Profile.objects.get(user=u)
        if row['Nickname'] == '-':
            p.name = row['Name']
        else:
            p.name = row['Nickname']
        p.college = row['College']
        p.dept = row['Dept']
        p.email_confirmed=True
        image_url = "https://api.adorable.io/avatars/"+ str(random.randint(0000,9999))
        full_path = 'media/images/' + username + '.png'
        try:
            urllib.request.urlretrieve(image_url, full_path)
        except:
            print("Downloadable Image Not Found!")
        p.image = '../' + full_path
        p.save()
        
        

        





