from django import template

register = template.Library()

from ..models import*
@register.filter(name='postlike_count')
def total_count(postid):
    postlikecount=PostLikes.objects.filter(post=postid,value=True).count()-PostLikes.objects.filter(post=postid,value=False).count()
    return(postlikecount)

@register.filter(name='userpostlike_count')
def user_count(postid,userid):
    userpostlike=PostLikes.objects.filter(post=postid,user=userid,value=True).count()-PostLikes.objects.filter(post=postid,user=userid,value=False).count()
    return(userpostlike)

@register.filter(name='usercommentlike_count')
def comment_count(replyid,userid):
    likes=Likes.objects.filter(reply=replyid,user=userid,value=True).count()-Likes.objects.filter(reply=replyid,user=userid,value=False).count()
    return(likes)

@register.filter(name='commentlike_count')
def commentlike_count(replyid):
    likes=Likes.objects.filter(reply=replyid,value=True).count()-Likes.objects.filter(reply=replyid,value=False).count()
    return(likes)