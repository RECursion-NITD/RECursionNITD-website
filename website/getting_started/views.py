from django.shortcuts import render
from getting_started.models import (
    Level,
    Topic,
    SubTopic,
    Note,
    File,
    Link,
)

def getting_started(request):

    levels = Level.objects.all().order_by('Number')
    topics = Topic.objects.all()
    subtopics = SubTopic.objects.all()
    notes = Note.objects.all()
    files = File.objects.all()
    links = Link.objects.all()

    args={'levels': levels,'topics': topics,'subtopics' : subtopics,'notes': notes, 'files': files, 'links': links}
    return render(request,'started.html',args)
