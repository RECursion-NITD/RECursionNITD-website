from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Experiences(models.Model):
    company = models.CharField(max_length=100)
    year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    job_profile = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_Rounds = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])
    interview_Questions = models.TextField()
    total_Compensation = models.PositiveIntegerField(
        blank=True, null=True
    )
    # TODO
    # AUTOGENERATE DATETIME
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.company

    def get_cname(self):
        class_name = "Experiences"
        return class_name

    class Meta:
        managed = True
        ordering = ['-created_at']
        db_table = 'experiences'
        verbose_name_plural = 'Experiences'
