from django.urls import path
from .views import *
from django.conf.urls import include,url
from django.conf import settings

urlpatterns = [
    path('add', add_question, name='add_question'),
    path('', list_questions ,name='list_questions'),
    path('detail/<int:id>/', detail_questions, name='detail_questions'),
    path('update/<int:id>/', update_questions, name='update_question'),
    path('follow/<int:id>/', edit_following, name='edit_following'),
]