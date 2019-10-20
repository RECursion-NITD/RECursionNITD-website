from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user_profile.models import *

@login_required
def add_experience(request):
    form = ExperienceForm(request.POST or None)
    if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            return redirect('interview_exp:list_experiences')

    return render(request, 'experience-form.html', {'form': form})

@login_required
def update_experience(request, id):
    try:
        experience = get_object_or_404(Experiences, pk=id)
    except:
        return HttpResponse("Content Does Not Exist :(")
    else:
        form = ExperienceForm(request.POST or None, instance = experience)

        if form.is_valid():
            form.save()
            return redirect('interview_exp:list_experiences')

    return render(request, 'experience-form.html', {'form': form, 'experience': experience})

def list_experiences(request):
    search = SearchForm(request.POST or None)
    if request.method == 'POST':
        if search.is_valid():
          key_req = search.cleaned_data
          key = key_req.get('key')
          return HttpResponseRedirect(reverse('interview_exp:search_experience', args=(key,)))
    experiences = Experiences.objects.all()
    paginator = Paginator(experiences, 5)
    page = request.GET.get('page')
    try:
        experiences_list = paginator.page(page)
    except PageNotAnInteger:
        experiences_list = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
            experiences_list = paginator.page(paginator.num_pages)
    ie_count = experiences.count()
    profiles = Profile.objects.all()
    args = {'form_search':search, 'profile':profiles, 'experiences': experiences_list, 'ie_count':ie_count}
    if request.is_ajax():
        return render(request, 'exp_list.html', args)
    return render(request, 'experiences.html', args)


def search_experience(request, key):
    print("I am yet to be done")

def detail_experiences(request, id):
    try:
        experience =get_object_or_404(Experiences, pk=id)
    except:
        return HttpResponse("Content Does Not Exist!")
    profile = Profile.objects.get(user=experience.user)
    args = {'experience': experience, 'profile': profile,}
    return render(request, 'exp_detail.html', args)