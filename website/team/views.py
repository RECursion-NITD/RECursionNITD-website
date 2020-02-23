from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *

# Create your views here.

def team_page(request):
    members = Members.objects.all()
    args={members: members}
    return render(request, 'team.html', args)
