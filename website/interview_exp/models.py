from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# Create your models here.

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Experiences(models.Model):
    company = models.CharField(max_length=100)
    year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    job_Profile = models.CharField(max_length=100)
    role_Type_choices = (
        ('Internship', 'Internship'),
        ('Full Time', 'Full Time'),
    )
    role_Type = models.CharField(max_length=50, choices=role_Type_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_Rounds = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])
    interview_Questions = models.TextField()
    interview_Questions = MarkdownxField()
    total_Compensation = models.PositiveIntegerField(
        blank=True, null=True
    )
    verification_Status_choices = (
        ('Approved', 'Approved'),
        ('Review Pending', 'Review Pending'),
        ('Changes Requested', 'Changes Requested'),
    )
    verification_Status = models.CharField(max_length=50, choices=verification_Status_choices, default='Review Pending')
    verifier = models.ForeignKey(User, related_name='verifier', on_delete=models.SET_NULL, null=True)
    # TODO
    # AUTOGENERATE DATETIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    @property
    def formatted_markdown(self):
        return markdownify(self.interview_Questions)
            
    def __str__(self):
        return str(self.company) + " " + str(self.user)

    def get_cname(self):
        class_name = "Experiences"
        return class_name

    class Meta:
        managed = True
        ordering = ['-created_at']
        db_table = 'experiences'
        verbose_name_plural = 'Experiences'


class Revisions(models.Model):
    experience = models.OneToOneField(Experiences, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    # TODO
    # AUTOGENERATE DATETIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return str(self.experience.company) + " " + str(self.reviewer)

    def get_cname(self):
        class_name = "Revisions"
        return class_name

    class Meta:
        managed = True
        ordering = ['-created_at']
        db_table = 'revisions'
        verbose_name_plural = 'Revisions'
