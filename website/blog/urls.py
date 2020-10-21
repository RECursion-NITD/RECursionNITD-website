from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url, include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add', views.add_blog, name='add_blog'),
    path('', views.list_blogs ,name='list_blogs'),
    path('detail/<int:id>/', views.detail_blogs, name='detail_blogs'),
    path('update/<int:id>/', views.update_blogs, name='update_blogs'),
    path('question/<int:id>/answer',views.add_reply,name='add_reply'),
    path('answer/<int:id>',views.update_reply,name='update_reply'),
    path('deleteanswer/<int:id>',views.delete_reply,name='delete_reply'),
    path('answer/<int:id>/vote', views.votings, name='votings'),
    path('comment/<int:id>/', views.add_comment, name='add_comment'),
    path('comment_answer/<int:id>/', views.add_comment_reply, name='add_comment_reply'),
    path('editcomment/<int:id>/',views.update_comment, name='update_comment'),
    path('editcomment_answer/<int:id>/', views.update_comment_reply, name='update_comment_reply'),
    path('deletecomment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('deletecomment_answer/<int:id>/', views.delete_reply_comment, name='delete_reply_comment'),
    path('filter/<int:id>/', views.filter_blog, name='filter_blog'),
    path('search/<str:key>', views.search_blog, name='search_blog'),
    url(r'^markdownx/', include('markdownx.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)