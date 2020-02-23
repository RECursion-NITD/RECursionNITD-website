from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *

# Create your views here.

def team_page(request):
    curr_batch_year = 2020
    members = Members.objects.all().order_by('name')
    args={members: members, curr_batch_year: curr_batch_year}
    return render(request, 'team/team.html', args)
