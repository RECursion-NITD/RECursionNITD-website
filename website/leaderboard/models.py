from django.db import models
from django.contrib.auth.models import User


class CPProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cp_profile'
    )
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, blank=True)
    college = models.CharField(
        max_length=200,
        default='National Institute of Technology, Durgapur'
    )
    batch = models.IntegerField(null=True, blank=True, db_index=True)
    dept = models.CharField(max_length=100, blank=True, db_index=True)

    # Codeforces
    codeforces_handle = models.CharField(max_length=100, blank=True, db_index=True)
    codeforces_rating = models.IntegerField(default=0, db_index=True)
    codeforces_max_rating = models.IntegerField(default=0)
    codeforces_rank = models.CharField(max_length=50, blank=True)
    codeforces_contests = models.IntegerField(default=0)
    codeforces_solved = models.IntegerField(default=0)
    codeforces_is_active = models.BooleanField(default=True, db_index=True)

    # CodeChef
    codechef_handle = models.CharField(max_length=100, blank=True, db_index=True)
    codechef_rating = models.IntegerField(default=0, db_index=True)
    codechef_stars = models.CharField(max_length=20, blank=True)
    codechef_global_rank = models.IntegerField(null=True, blank=True)
    codechef_contests = models.IntegerField(default=0)
    codechef_is_active = models.BooleanField(default=True, db_index=True)

    # LeetCode
    leetcode_handle = models.CharField(max_length=100, blank=True)
    leetcode_rating = models.IntegerField(default=0, db_index=True)
    leetcode_solved = models.IntegerField(default=0)

    # Codolio
    codolio_handle = models.CharField(max_length=100, blank=True)
    codolio_cscore = models.FloatField(default=0.0, db_index=True)

    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_synced = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-codeforces_rating', '-codechef_rating']
        verbose_name = 'CP Profile'
        verbose_name_plural = 'CP Profiles'

    def __str__(self):
        return f"{self.name} (CF: {self.codeforces_handle or 'N/A'}, CC: {self.codechef_handle or 'N/A'})"
