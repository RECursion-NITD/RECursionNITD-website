#import python's built-in csv library
from django.contrib.auth.models import User
from forum.models import *
from forum.views import bulk_tagging_add
import urllib.request
import random
import csv
import datetime


randhash = "abcdef"
# open the file in read mode
with open('import_scripts/answers.csv', 'r') as csvfile:

    # convert the data in this file into a DictReader
    error_list = []
    reader = csv.DictReader(csvfile,delimiter = ';')
    for row in reader:
        print(row['Title [Question]'])
        
        try:
            user = User.objects.filter(email = row['Email [User]'])[0]
            
            question = Questions.objects.filter(title = row['Title [Question]'])[0]
            ans = Answers(description = row['Description'],user_id=user,question_id = question)
            ans.save()
        except:
            error_list.append(row['Title [Question]'])
        
    print(error_list)
