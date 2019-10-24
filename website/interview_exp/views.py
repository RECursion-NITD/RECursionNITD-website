from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user_profile.models import *
from difflib import SequenceMatcher


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


@login_required
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
    ie_count = len(experiences)
    profiles = Profile.objects.all()
    args = {'form_search':search, 'profile':profiles, 'experiences': experiences_list, 'ie_count':ie_count}
    if request.is_ajax():
        return render(request, 'exp_list.html', args)
    return render(request, 'experiences.html', args)


@login_required
def search_experience(request, key):
    experiences_list = Experiences.objects.all()
    experiences_found = []
    for experience in experiences_list:
        if SequenceMatcher(None, experience.company.lower(), key.lower()).ratio() > 0.4:
            experiences_found.append([SequenceMatcher(None, experience.company.lower(), key.lower()).ratio(), experience])
        if SequenceMatcher(None, str(experience.year), key.lower()).ratio() > 0.5:
            experiences_found.append([SequenceMatcher(None, str(experience.year), key.lower()).ratio(), experience])
    experiences_found.sort(key=lambda x: x[0], reverse=True)
    experiences = []
    for experience in experiences_found:
        if experience[1] not in experiences:
            experiences.append(experience[1])


    search = SearchForm(request.POST or None)
    if request.method == 'POST':
        if search.is_valid():
            key_req = search.cleaned_data
            key = key_req.get('key')
            return HttpResponseRedirect(reverse('interview_exp:search_experience', args=(key,)))
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
    ie_count = len(experiences)
    profiles = Profile.objects.all()
    args = {'form_search': search, 'profile': profiles, 'experiences': experiences_list, 'ie_count': ie_count}
    if request.is_ajax():
        return render(request, 'exp_list.html', args)
    return render(request, 'experiences.html', args)


@login_required
def detail_experiences(request, id):
    try:
        experience =get_object_or_404(Experiences, pk=id)
    except:
        return HttpResponse("Content Does Not Exist!")
    profile = Profile.objects.get(user=experience.user)
    args = {'experience': experience, 'profile': profile,}
    return render(request, 'exp_detail.html', args)