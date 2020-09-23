from django.shortcuts import render
from .models import*
from user_profile.models import*
from django.views.generic import ListView

def blog(request):
    context={
            'posts':Posts.objects.all().order_by('-created_at'),
    }
    return render(request,'blog/blog_page.html',context)


def list_blogs(request):
    search = SearchForm(request.POST or None)
    if request.method == 'POST':
        if search.is_valid():
          key_req = search.cleaned_data
          key = key_req.get('key')
          return HttpResponseRedirect(reverse('forum:search_question', args=(key,)))
    posts = Posts.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts_list = paginator.page(paginator.num_pages)
    post_count=posts.count()
    replies=Reply.objects.all()
    taggings_recent = Taggings.objects.all().order_by('-updated_at')
    tags_recent=Tags.objects.all().order_by('-updated_at')
    tags_popular=[]
    check = []
    #Keeping the count of tags atmost 10
    if tags_recent.count()>10:
        limit=10
    else:
        limit=tags_recent.count()
    for tag in tags_recent:
        tagging = Taggings.objects.filter(tag=tag)
        count=tagging.count()
        tags_popular.append([count,tag])
        if count>0:
            check.append(tag)
    tags_popular.sort(key=lambda x: x[0],reverse=True)
    tags_recent_record=[]
    tags_popular_record=[]
    for i in range(limit):
        tags_popular_record.append(tags_popular[i][1])
    count=0
    # import pdb;pdb.set_trace();
    while len(tags_recent_record)< len(taggings_recent) and len(tags_recent_record)< len(check) and len(tags_recent_record) < 10:
        if taggings_recent[count].tag not in tags_recent_record:
           tags_recent_record.append(taggings_recent[count].tag)
        count+=1
    profiles=Profile.objects.all()
    args = {'form_search':search, 'profile':profiles, 'posts':post_list, 'replies':replies, 'tags':tags_recent, 'taggings':taggings_recent, 'tags_recent':tags_recent_record, 'tags_popular':tags_popular_record, 'p_count':post_count,'limit':limit}
    if request.is_ajax():
        return render(request, 'blog_list.html', args)
    return render(request, 'blog_page.html', args)