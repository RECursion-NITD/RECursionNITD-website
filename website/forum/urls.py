from django.urls import path
from .views import *
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static
from user_profile import urls

app_name="forum"
urlpatterns = [
    #path('document/',farewell,name='farewell'),
    path('profile/', include('user_profile.urls')),
    #path('start/', getting_started, name='getting_started'),
    path('team/', team_page, name='team_page'),
    path('webdteam/', webd_team, name='webd_team'),
    path('faculty/', faculty, name='faculty'),
    path('add', add_question, name='add_question'),
    path('', list_questions ,name='list_questions'),
    path('detail/<int:id>/', detail_questions, name='detail_questions'),
    path('update/<int:id>/', update_questions, name='update_question'),
    path('question/<int:id>/answer',add_answer,name='add_answer'),
    path('answer/<int:id>',update_answer,name='update_answer'),
    path('deleteanswer/<int:id>',delete_answer,name='delete_answer'),
    path('answer/<int:id>/vote', voting, name='voting'),
    path('follow/<int:id>/', edit_following, name='edit_following'),
    path('comment/<int:id>/', add_comment, name='add_comment'),
    path('comment_answer/<int:id>/', add_comment_answer, name='add_comment_answer'),
    path('editcomment/<int:id>/', update_comment, name='update_comment'),
    path('editcomment_answer/<int:id>/', update_comment_answer, name='update_comment_answer'),
    path('deletecomment/<int:id>/', delete_comment, name='delete_comment'),
    path('deletecomment_answer/<int:id>/', delete_answer_comment, name='delete_answer_comment'),
    path('filter/<int:id>/', filter_question, name='filter_question'),
    path('search/<str:key>', search_question, name='search_question'),
    url(r'^markdownx/', include('markdownx.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
