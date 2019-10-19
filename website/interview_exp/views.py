from django.shortcuts import render, redirect,get_object_or_404, get_list_or_404
from .models import *
from .forms import ExperienceForm
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