from django.contrib import admin
from .models import*

blog_models=[Posts,Reply,Comment,Comment_Reply,Like,Tags,Taggings]
admin.site.register(blog_models)