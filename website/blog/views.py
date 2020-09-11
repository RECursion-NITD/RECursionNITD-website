from django.shortcuts import render

def blog(request):
    return render(request,'blog/blog_page.html')