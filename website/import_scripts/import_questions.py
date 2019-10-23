
from django.contrib.auth.models import User
from forum.models import *
from forum.views import bulk_tagging_add
import urllib.request
import random
import csv
import datetime


randhash = "abcdef"
# open the file in read mode
with open('import_scripts/question.csv', 'r') as csvfile:

    # convert the data in this file into a DictReader
    reader = csv.DictReader(csvfile,delimiter = ';')
    for row in reader:
        print(row['Title'])
        created = datetime.datetime.strptime(row['Created at'], '%B %d, %Y %H:%M')
        updated = datetime.datetime.strptime(row['Updated at'], '%B %d, %Y %H:%M')
        print(row['Email [User]'])
        user = User.objects.get(email = row['Email [User]'])
        q = Questions(title = row['Title'],description = row['Description'],user_id = user,created_at = created ,updated_at = updated)
        q.save()
        tags = row['Name [Tags]'].split(',')
        tag_objects = []
        for tag in tags:
            result = Tags.objects.filter(name = tag)
            if result.exists():
                tag_objects.append(result[0])
            else:
                tag_objects.append(Tags.objects.create(name=tag))
        bulk_tagging_add(q,tag_objects)
    