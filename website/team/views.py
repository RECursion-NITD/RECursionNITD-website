from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *

# Create your views here.

def team_page(request):
    today = datetime.datetime.now()
    month = today.month
    year = today.year

    if month==6 or month == 7 or month == 8 or month == 9 or month == 10 or month == 11 or month == 12:
        curr_batch_year = year + 1
    else:
        curr_batch_year = year

    members = Members.objects.all().filter(batch_year__range=[curr_batch_year, 2050]).order_by('batch_year', 'name')
    alumni = Members.objects.all().filter(batch_year__range=[2016, curr_batch_year - 1]).order_by('-batch_year', 'name')

    year_set = []
    for a in alumni:
        if a.batch_year not in year_set:
            year_set.append(a.batch_year)

    presi = Members.objects.filter(batch_year = curr_batch_year, designation = "President")
    convener = Members.objects.filter(batch_year=curr_batch_year, designation="Convener")
    treasurer = Members.objects.filter(batch_year=curr_batch_year, designation="Treasurer")
    vice_presi = Members.objects.filter(batch_year=curr_batch_year, designation="Vice President")
    gen_sec = Members.objects.filter(batch_year=curr_batch_year, designation="General Secretary")
    args={'members': members, 'alumni': alumni, 'curr_batch_year': curr_batch_year, 'year_set': year_set, 'presi': presi, 'convener': convener, 'treasurer': treasurer, 'vice_presi': vice_presi, 'gen_sec': gen_sec}
    return render(request, 'team/team.html', args)
