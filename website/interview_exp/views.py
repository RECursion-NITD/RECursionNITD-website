from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user_profile.models import *
from difflib import SequenceMatcher
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail


@login_required
def add_experience(request):
    form = ExperienceForm(request.POST or None)
    if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()

            profiles = Profile.objects.filter(~Q(role = '3'))
            messages = ()
            for profile in profiles:
                user = profile.user
                current_site = get_current_site(request)
                subject = 'New Activity in Interview Experiences Section'
                message = render_to_string('new_experience_entry_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'experience': Experiences.objects.get(pk=f.id),
                })
                msg = (subject, message, 'webmaster@localhost', [user.email])
                if msg not in messages:
                    messages += (msg,)
            result = send_mass_mail(messages, fail_silently=False)

            return redirect('interview_exp:list_experiences')

    if form.errors:
        return render(request, 'experience-form.html', {'form': form})      

    return render(request, 'experience-form.html', {'form': form})


@login_required
def update_experience(request, id):
    current_user_profile = Profile.objects.get(user = request.user)
    try:
        experience = get_object_or_404(Experiences, pk=id)
    except:
        return render(request,'id_error.html',{'experience':1})
    else:
        if experience.user != request.user and current_user_profile.role != '1':
            return redirect('interview_exp:list_experiences')
        form = ExperienceForm(request.POST or None, instance = experience)

        if form.is_valid():
            form.save()
            flag = 0
            if experience.verification_Status == 'Approved':
                experience.verification_Status = 'Review Pending'
                flag = 1
            experience.save()

            if experience.verification_Status == 'Changes Requested':
                revision = Revisions.objects.get(experience = experience)
                profile = Profile.objects.get(user = revision.reviewer)
                messages = ()
                user = profile.user
                current_site = get_current_site(request)
                subject = 'New Activity in Interview Experiences Section'
                message = render_to_string('update_experience_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'experience': Experiences.objects.get(pk=experience.id),
                })
                msg = (subject, message, 'webmaster@localhost', [user.email])
                if msg not in messages:
                    messages += (msg,)
                result = send_mass_mail(messages, fail_silently=False)

            elif experience.verification_Status == 'Review Pending' and flag == 1:
                profiles = Profile.objects.filter(~Q(role='3'))
                messages = ()
                for profile in profiles:
                    user = profile.user
                    current_site = get_current_site(request)
                    subject = 'New Activity in Interview Experiences Section'
                    message = render_to_string('update_Experience_to_all_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'experience': Experiences.objects.get(pk=experience.id),
                    })
                    msg = (subject, message, 'webmaster@localhost', [user.email])
                    if msg not in messages:
                        messages += (msg,)
                result = send_mass_mail(messages, fail_silently=False)

            return redirect('interview_exp:list_experiences')

        if form.errors:
            return render(request, 'experience-form.html', {'form': form})       

    return render(request, 'experience-form.html', {'form': form, 'experience': experience})


@login_required
def list_experiences(request):
    search = SearchForm(request.POST or None)
    if request.method == 'POST':
        if search.is_valid():
          key_req = search.cleaned_data
          key = key_req.get('key')
          return HttpResponseRedirect(reverse('interview_exp:search_experience', args=(key,)))
    current_user_profile = Profile.objects.get(user = request.user)
    if current_user_profile.role == '1' or current_user_profile.role == '2':
       experiences = Experiences.objects.all()
    else:
       experiences = Experiences.objects.filter(Q(user = request.user) | Q(verification_Status = 'Approved'))
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
    current_user_profile = Profile.objects.get(user=request.user)
    if current_user_profile.role == '1' or current_user_profile.role == '2':
       experiences_list = Experiences.objects.all()
    else:
       experiences_list = Experiences.objects.filter(Q(user = request.user) | Q(verification_Status = 'Approved'))
    experiences_found = []
    for experience in experiences_list:
        if SequenceMatcher(None, experience.company.lower(), key.lower()).ratio() > 0.4:
            experiences_found.append([SequenceMatcher(None, experience.company.lower(), key.lower()).ratio(), experience])
        if SequenceMatcher(None, str(experience.year), key.lower()).ratio() > 0.5:
            experiences_found.append([SequenceMatcher(None, str(experience.year), key.lower()).ratio(), experience])
        if SequenceMatcher(None, experience.user.username.lower(), key.lower()).ratio() > 0.5:
            experiences_found.append([SequenceMatcher(None, experience.user.username.lower(), key.lower()).ratio(), experience])
    profiles = Profile.objects.all()
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
    args = {'form_search': search, 'profile': profiles, 'experiences': experiences_list, 'ie_count': ie_count}
    if request.is_ajax():
        return render(request, 'exp_list.html', args)
    return render(request, 'experiences.html', args)

@login_required
def filter_experience(request, role):
    search = SearchForm(request.POST or None)
    if request.method == 'POST':
        if search.is_valid():
          key_req = search.cleaned_data
          key = key_req.get('key')
          return HttpResponseRedirect(reverse('interview_exp:search_experience', args=(key,)))

    current_user_profile = Profile.objects.get(user=request.user)
    if current_user_profile.role == '1' or current_user_profile.role == '2':
        experiences_list = Experiences.objects.all()
    else:
        experiences_list = Experiences.objects.filter(Q(user=request.user) | Q(verification_Status='Approved'))

    if role == 'All':
       experiences = experiences_list
    else:
        experiences = experiences_list.filter(role_Type=role)
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
def detail_experiences(request, id):
    current_user_profile = Profile.objects.get(user = request.user)
    try:
        experience =get_object_or_404(Experiences, pk=id)
    except:
        return render(request,'id_error.html',{'experience':1})
    if experience.verification_Status != 'Approved' and experience.user != request.user and current_user_profile.role == '3':
        return redirect('interview_exp:list_experiences')
    profile = Profile.objects.get(user=experience.user)
    user_permission = current_user_profile.role == '1' or current_user_profile.role == '2'
    exp_update_perms = current_user_profile.role == '1' or experience.user == request.user
    if experience.verification_Status == 'Changes Requested':
      revision = Revisions.objects.get(experience = experience)
      args = {'experience': experience, 'profile': profile, 'user_permission': user_permission, 'revision': revision, 'exp_update_perms': exp_update_perms,}
    else:
        args = {'experience': experience, 'profile': profile, 'user_permission': user_permission, 'exp_update_perms': exp_update_perms,}
    return render(request, 'exp_detail.html', args)


@login_required
def revise_experience(request, id, action):
    try:
        experience = get_object_or_404(Experiences, pk=id)
    except:
        return render(request,'id_error.html',{'experience':1})

    if experience.verification_Status == 'Approved':
        return HttpResponseRedirect(reverse('interview_exp:detail_experiences', args=(id,)))

    current_user_profile = Profile.objects.get(user = request.user)
    if current_user_profile.role == '3':
        return HttpResponseRedirect(reverse('interview_exp:detail_experiences', args=(id,)))

    if action == 'Accept':
        experience.verification_Status = 'Approved'
        experience.verifier = request.user
        experience.save()

        if Revisions.objects.filter(experience = experience).exists():
            revision = Revisions.objects.get(experience = experience)
            revision.delete()

        return HttpResponseRedirect(reverse('interview_exp:detail_experiences', args=(id,)))

    elif action == 'Reject':

        if experience.verification_Status == 'Review Pending':
            form = RevisionForm(request.POST or None)
            if form.is_valid():
                f = form.save(commit=False)
                f.experience = experience
                f.reviewer = request.user
                f.save()

                experience.verification_Status = 'Changes Requested'
                experience.save()

                profile = Profile.objects.get(user=experience.user)
                messages = ()
                user = profile.user
                current_site = get_current_site(request)
                subject = 'New Activity in Interview Experiences Section'
                message = render_to_string('changes_requested_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'experience': Experiences.objects.get(pk=experience.id),
                })
                msg = (subject, message, 'webmaster@localhost', [user.email])
                if msg not in messages:
                    messages += (msg,)
                result = send_mass_mail(messages, fail_silently=False)

                return HttpResponseRedirect(reverse('interview_exp:detail_experiences', args=(id,)))
            return render(request, 'revision-form.html', {'form': form})

        elif experience.verification_Status == 'Changes Requested':
            revision = Revisions.objects.get(experience = experience)
            form = RevisionForm(request.POST or None, instance=revision)

            if form.is_valid():
                f = form.save(commit=False)
                f.reviewer = request.user
                f.save()

                profile = Profile.objects.get(user=experience.user)
                messages = ()
                user = profile.user
                current_site = get_current_site(request)
                subject = 'New Activity in Interview Experiences Section'
                message = render_to_string('changes_requested_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'experience': Experiences.objects.get(pk=experience.id),
                })
                msg = (subject, message, 'webmaster@localhost', [user.email])
                if msg not in messages:
                    messages += (msg,)
                result = send_mass_mail(messages, fail_silently=False)

                return HttpResponseRedirect(reverse('interview_exp:detail_experiences', args=(id,)))

            return render(request, 'revision-form.html', {'form': form})



