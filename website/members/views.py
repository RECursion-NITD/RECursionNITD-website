from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render, redirect
from members.models import Members
from django.contrib.auth.models import User
from . import forms
# Create your views here.



def member_list(request):

	members = Members.objects.all().order_by('year_of_graduation')
	args={'form' : forms.CreateMember , 'members' : members}
	return render(request, 'members/members_list.html' , args)
def member_create(request):
	if request.method == "POST":

		form=forms.CreateMember(request.POST,request.FILES)

		if form.is_valid():
			#save member to database
			new_member=form.save(commit=False)
			new_member.save()
			return redirect('members:list')
		else:
			return render(request,'members/members_create.html',{'form':form})


	else:
		form=forms.CreateMember()
		return render(request,'members/members_create.html',{'form':form})

def member_edit(request, id=None):
	member=get_object_or_404(Members,id=id)
	form = forms.CreateMember(request.POST or None, instance=member)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('members:list')

	else:
		return render(request, 'members/members_edit.html',{'form':form}) 

def member_delete(request, id=None):
	member=get_object_or_404(Members,id=id)
	if request.method == 'GET':
		member.delete()
		return redirect('members:list')




