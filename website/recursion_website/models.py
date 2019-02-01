# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Done
class Questions(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    # TODO
    # AUTOGENERATE DATETIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    visibility = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    class Meta:
        managed = True
        ordering = ['-created_at']
        db_table = 'questions'
        verbose_name_plural = 'Questions'


# Done
class Answers(models.Model):
    description = models.TextField()
    # TODO :
    # DATE TIME auto-generated
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question_id = models.ForeignKey(Questions, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.description
    class Meta:
        managed = True
        db_table = 'answers'
        verbose_name_plural = 'Answers'


# # TBD
# class ArInternalMetadata(models.Model):
#     key = models.CharField(primary_key=True, max_length=-1)
#     value = models.CharField(max_length=-1, blank=True, null=True)
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()

#     class Meta:
#         managed = True
#         db_table = 'ar_internal_metadata'

# Consult with anand
# class CkeditorAssets(models.Model):
#     data_file_name = models.CharField(max_length=-1)
#     data_content_type = models.CharField(max_length=-1, blank=True, null=True)
#     data_file_size = models.IntegerField(blank=True, null=True)
#     e_type = models.CharField(max_length=30, blank=True, null=True)
#     width = models.IntegerField(blank=True, null=True)
#     height = models.IntegerField(blank=True, null=True)
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()

#     class Meta:
#         managed = True
#         db_table = 'ckeditor_assets'




class Comments(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, models.DO_NOTHING)
    question = models.ForeignKey(Questions, models.DO_NOTHING)
    # TO DO
    # AUTOGEN DATETIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.body

    class Meta:
        managed = True
        db_table = 'comments'
        verbose_name_plural = 'Comments'

       
class Comments_Answers(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, models.DO_NOTHING)
    answer = models.ForeignKey(Answers, models.DO_NOTHING)
    # TO DO
    # AUTOGEN DATETIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.body

    class Meta:
        managed = True
        db_table = 'comments_answers'
        verbose_name_plural = 'Comments_Answers'


# DONE
class Follows(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey('Questions', on_delete=models.CASCADE)
    # TODO
    # AUTOGEN DATETIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.id) + str(self.user)

    class Meta:
        managed = True
        db_table = 'follows'
        verbose_name_plural = 'Follows'


# class Identities(models.Model):
#     uid = models.CharField(max_length=-1, blank=True, null=True)
#     provider = models.CharField(max_length=-1, blank=True, null=True)
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()
#     user_id = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'identities'



# class SchemaMigrations(models.Model):
#     version = models.CharField(primary_key=True, max_length=-1)

#     class Meta:
#         managed = True
#         db_table = 'schema_migrations'


# DONE
class Tags(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    # TBD
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        if self.name== None:
            return "None"
        else:
            return self.name

    class Meta:
        managed = True
        db_table = 'tags'
        verbose_name_plural = ' Tags'


class Taggings(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=True, null=True)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, blank=True, null=True)
    # TBD
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.question.title + " : " + self.tag.name

    class Meta:
        managed = True
        db_table = 'taggings'
        verbose_name_plural = 'Taggings'


# DONE


# DONE
class Upvotes(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    answer = models.ForeignKey(Answers, models.DO_NOTHING)
    # TBD
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    def __self__(self):
        return self.user
    class Meta:
        managed = True
        db_table = 'upvotes'
        verbose_name_plural = 'Upvotes'


"""
TODO
- Roles : list containing tuples, with various grant level
    Choice field.
"""
