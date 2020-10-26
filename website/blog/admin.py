from django.contrib import admin
from .models import *

blog_models=[Posts,Likes,Taggings,Tags,Comment_Reply,Comment,Reply]
admin.site.register(blog_models)