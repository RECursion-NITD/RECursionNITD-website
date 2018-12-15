from django.urls import path
from .views import *


urlpatterns = [
    path('', list_questions ,name='list_questions'),
    #path('new', create_question , name='create_questions'),
    path('detail/<int:id>/', detail_questions, name='detail_questions'),
    path('update/<int:id>/', update_questions, name='update_questions'),
]