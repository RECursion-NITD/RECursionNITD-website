from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from difflib import SequenceMatcher
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail

# Create your views here.

def team_page(request):
    print("Hey")
    #members = Members.objects.all()
    #args={}
    #return render(request, 'getting_started.html', args)
