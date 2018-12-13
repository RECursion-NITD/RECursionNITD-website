from django.contrib import admin
from django.urls import path
from . import views

app_name = 'recursion_website'

urlpatterns = [
	path('list/', views.member_list, name="list"),
    path('create/',views.member_create, name="create"),
    path('<int:id>/edit/',views.member_edit, name="edit"),
    path('<int:id>/delete/',views.member_delete, name="delete")
]