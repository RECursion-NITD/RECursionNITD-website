from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
from .forms import ExperienceForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


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
            return redirect('interview_exp:list_questions')

    return render(request, 'experience-form.html', {'form': form, 'experience': experience})