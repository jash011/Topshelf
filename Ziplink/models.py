from django.db import models
from django.contrib.auth.models import User
class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.TextField()
    short_url = models.CharField(max_length=225, unique=True)
    clicks = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    sl_id = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.short_url
