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
with open('import_scripts/question.csv', 'r') as csvfile:

    # convert the data in this file into a DictReader
    reader = csv.DictReader(csvfile,delimiter = ';')
    for row in reader:
        print(row['Title [Question]'])
        
