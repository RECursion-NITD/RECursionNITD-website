from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Done
class Posts(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_cname(self):
        class_name = "Post"
        return class_name

    class Meta:
        verbose_name_plural="Posts"

class Reply(models.Model):
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
    
    def get_cname(self):
        class_name = "Reply"
        return class_name
    
    class Meta:
        verbose_name_plural="Reply"


class Comment(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    # TO DO
    # AUTOGEN DATETIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.body
    
    def get_cname(self):
        class_name = "C"
        return class_name
    
    class Meta:
        verbose_name_plural="Comment"


       
class Comment_Reply(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.body
    
    def get_cname(self):
        class_name = "Comment_Reply"
        return class_name
    class Meta:
        verbose_name_plural="Comment_Reply"


class Tags(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        if self.name== None:
            return "None"
        else:
            return self.name
    class Meta:
        verbose_name_plural="Tags"





class Taggings(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, blank=True, null=True)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.post.title + " : " + self.tag.name
    
    class Meta:
        verbose_name_plural="Taggings"


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    # TBD
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    value = models.BooleanField(null=True,blank=True)

    def __self__(self):
        return self.user
    
    class Meta:
        verbose_name_plural="Comment_Likes"



class PostLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    # TBD
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    value = models.BooleanField(null=True,blank=True)

    def __self__(self):
        return self.user
    
    class Meta:
        verbose_name_plural="Post_Likes"
