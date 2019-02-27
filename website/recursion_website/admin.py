from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
   #readonly_fields = ['created_at','updated_at','user_id']
   pass

@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Answers)
class AnswerAdmin(admin.ModelAdmin):
    pass

@admin.register(Taggings)
class TaggingAdmin(admin.ModelAdmin):
    pass

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Upvotes)
class UpvoteAdmin(admin.ModelAdmin):
    pass

@admin.register(Follows)
class FollowAdmin(admin.ModelAdmin):
    pass

@admin.register(Comments_Answers)
class Comments_AnswerAdmin(admin.ModelAdmin):
    pass

