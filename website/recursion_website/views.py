from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render, redirect
from recursion_website.models import Members
from django.contrib.auth.models import User
from . import forms
# Create your views here.
def member_list(request):

	members = Members.objects.all().order_by('id')
	args={'form' : forms.CreateMember , 'members' : members}
	return render(request, 'recursion_website/members/members_list.html' , args)
def member_create(request):
	if request.method == "POST":
		form=forms.CreateMember(request.POST)
		if form.is_valid():
			#save member to database
			new_member=form.save(commit=False)
			new_member.save()
			return redirect('recursion_website:list')

	else:
		form=forms.CreateMember()
		return render(request,'recursion_website/members/members_create.html',{'form':form})

def member_edit(request, id=None):
	member=get_object_or_404(Members,id=id)
	form = forms.CreateMember(request.POST or None, instance=member)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('recursion_website:list')

	else:
		return render(request, 'recursion_website/members/members_edit.html',{'form':form}) 

def member_delete(request, id=None):
	member=get_object_or_404(Members,id=id)
	if request.method == 'GET':
		member.delete()
		return redirect('recursion_website:list')




