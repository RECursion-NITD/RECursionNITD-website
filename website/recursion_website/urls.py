from django.urls import path
from .views import *
from django.conf.urls import include,url
from django.conf import settings

urlpatterns = [
    path('add', add_question, name='add_question'),
    path('', list_questions ,name='list_questions'),
    path('detail/<int:id>/', detail_questions, name='detail_questions'),
    path('update/<int:id>/', update_questions, name='update_question'),

    path('question/<int:id>/answer',add_answer,name='add_answer'),
    path('answer/<int:id>',update_answer,name='update_answer'),
    path('answer/<int:id>/vote', voting, name='voting'),
    path('follow/<int:id>/', edit_following, name='edit_following'),
    path('comment/<int:id>/', add_comment, name='add_comment'),
    path('editcomment/<int:id>/', update_comment, name='update_comment'),
]
