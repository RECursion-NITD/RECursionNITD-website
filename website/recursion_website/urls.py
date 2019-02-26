from django.urls import path
from .views import *
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add', add_question, name='add_question'),
    path('', list_questions ,name='list_questions'),
    path('detail/<int:id>/', detail_questions, name='detail_questions'),
    path('update/<int:id>/', update_questions, name='update_question'),
    path('viewprofile/<int:id>/', view_profile, name='view_profile'),
    path('question/<int:id>/answer',add_answer,name='add_answer'),
    path('answer/<int:id>',update_answer,name='update_answer'),
    path('answer/<int:id>/vote', voting, name='voting'),
    path('follow/<int:id>/', edit_following, name='edit_following'),
    path('comment/<int:id>/', add_comment, name='add_comment'),
    path('comment_answer/<int:id>/', add_comment_answer, name='add_comment_answer'),
    path('editcomment/<int:id>/', update_comment, name='update_comment'),
    path('editcomment_answer/<int:id>/', update_comment_answer, name='update_comment_answer'),
    path('register/', user_register, name="user_register"),
    path('editprofile/', edit_profile, name='edit_profile'),
    path('filter/<int:id>/', filter_question, name='filter_question'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        activate, name='activate'),
    path('change_password/', change_password, name='change_password'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset/done/', password_reset_done, name='password_reset_done'),
    path('reset/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', password_reset_complete, name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
