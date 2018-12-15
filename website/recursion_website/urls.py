from . import views
from django.conf.urls import include,url
from django.conf import settings
from django.urls import path


urlpatterns = [
               
                url(r'add_question/$',views.add_question,name = 'add_question'),
                 path('',views.list_questions ,name='list_questions'),
                path('detail/<int:id>/',views.detail_questions, name='detail_questions'),
                 path('update/<int:id>/',views.update_questions, name='update_questions'),
               
              ]