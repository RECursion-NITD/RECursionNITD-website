from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
import datetime
from django.http import JsonResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

# Create your views here.

def team_page(request):
    today = datetime.datetime.now()
    month = today.month
    year = today.year

    if month==6 or month == 7 or month == 8 or month == 9 or month == 10 or month == 11 or month == 12:
        curr_batch_year = year + 1
    else:
        curr_batch_year = year

    # Get 4th year members in specific order
    position_order = ['President', 'Vice President', 'Treasurer', 'Convener', 'General Secretary']
    flagbearers = []
    
    # Add members in position order first
    for position in position_order:
        members_with_position = Members.objects.filter(batch_year=curr_batch_year, designation=position).order_by('name')
        flagbearers.extend(members_with_position)
    
    # Add remaining members
    other_members = Members.objects.filter(batch_year=curr_batch_year).exclude(designation__in=position_order).order_by('name')
    flagbearers.extend(other_members)
    
    # Get 3rd and 2nd year members (coordinators)
    coordinators = Members.objects.filter(batch_year__in=[curr_batch_year + 1, curr_batch_year + 2]).order_by('batch_year', 'name')
    
    args={'flagbearers': flagbearers, 'coordinators': coordinators, 'curr_batch_year': curr_batch_year}
    return render(request, 'team/team.html', args)

def alumni_page(request):
    today = datetime.datetime.now()
    month = today.month
    year = today.year

    if month==6 or month == 7 or month == 8 or month == 9 or month == 10 or month == 11 or month == 12:
        curr_batch_year = year + 1
    else:
        curr_batch_year = year
    
    # Get alumni data
    alumni = Members.objects.filter(batch_year__range=[2016, curr_batch_year - 1]).order_by('-batch_year', 'name')
    year_set = []
    for a in alumni:
        if a.batch_year not in year_set:
            year_set.append(a.batch_year)
    
    args={'alumni': alumni, 'year_set': year_set}
    return render(request, 'team/alumni.html', args)

# API Endpoints for React Frontend
@csrf_exempt
def team_api(request):
    today = datetime.datetime.now()
    month = today.month
    year = today.year

    if month in [6,7,8,9,10,11,12]:
        curr_batch_year = year + 1
    else:
        curr_batch_year = year

    # Get flagbearers in order
    position_order = ['President', 'Vice President', 'Treasurer', 'Convener', 'General Secretary']
    flagbearers_data = []
    
    for position in position_order:
        members = Members.objects.filter(batch_year=curr_batch_year, designation=position).order_by('name')
        for member in members:
            flagbearers_data.append({
                'id': member.id,
                'name': member.name,
                'designation': member.designation,
                'branch': member.branch,
                'batch_year': member.batch_year,
                'image': member.image.url if member.image else None,
                'facebook': member.url_Facebook,
                'linkedin': member.url_LinkedIn,
                'mobile': member.mobile
            })
    
    # Add other members
    other_members = Members.objects.filter(batch_year=curr_batch_year).exclude(designation__in=position_order).order_by('name')
    for member in other_members:
        flagbearers_data.append({
            'id': member.id,
            'name': member.name,
            'designation': member.designation,
            'branch': member.branch,
            'batch_year': member.batch_year,
            'image': member.image.url if member.image else None,
            'facebook': member.url_Facebook,
            'linkedin': member.url_LinkedIn,
            'mobile': member.mobile
        })
    
    # Get coordinators
    coordinators_data = []
    coordinators = Members.objects.filter(batch_year__in=[curr_batch_year + 1, curr_batch_year + 2]).order_by('batch_year', 'name')
    for member in coordinators:
        role = 'Senior Coordinator' if member.batch_year == curr_batch_year + 1 else 'Junior Coordinator'
        coordinators_data.append({
            'id': member.id,
            'name': member.name,
            'designation': role,
            'branch': member.branch,
            'batch_year': member.batch_year,
            'image': member.image.url if member.image else None,
            'facebook': member.url_Facebook,
            'linkedin': member.url_LinkedIn,
            'mobile': member.mobile
        })
    
    return JsonResponse({
        'flagbearers': flagbearers_data,
        'coordinators': coordinators_data,
        'current_batch_year': curr_batch_year
    }, safe=False)

@csrf_exempt
def alumni_api(request):
    today = datetime.datetime.now()
    month = today.month
    year = today.year

    if month in [6,7,8,9,10,11,12]:
        curr_batch_year = year + 1
    else:
        curr_batch_year = year
    
    alumni = Members.objects.filter(batch_year__range=[2016, curr_batch_year - 1]).order_by('-batch_year', 'name')
    alumni_data = []
    year_set = []
    
    for member in alumni:
        if member.batch_year not in year_set:
            year_set.append(member.batch_year)
        
        alumni_data.append({
            'id': member.id,
            'name': member.name,
            'designation': member.designation,
            'branch': member.branch,
            'batch_year': member.batch_year,
            'image': member.image.url if member.image else None,
            'facebook': member.url_Facebook,
            'linkedin': member.url_LinkedIn,
            'mobile': member.mobile
        })
    
    return JsonResponse({
        'alumni': alumni_data,
        'yearSet': sorted(year_set, reverse=True)
    }, safe=False)
