from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
   #readonly_fields = ['created_at','updated_at','user_id']
   pass

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass

@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    pass

@admin.register(Taggings)
class TaggingsAdmin(admin.ModelAdmin):
    pass

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass

@admin.register(Upvotes)
class UpvotesAdmin(admin.ModelAdmin):
    pass

@admin.register(Follows)
class FollowsAdmin(admin.ModelAdmin):
  pass


