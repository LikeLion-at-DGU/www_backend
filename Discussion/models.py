from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime

def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

# Discussion 글
class Discussion(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.title

# 글에 대한 투표 항목
class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    # discussion -> default = ' ', null = True (추가)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="choices", default='', null=True)
    vote_item = models.CharField(max_length=30)
    voted_user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    cnt = models.IntegerField(default=0)

# Discussion 댓글
class DComment(models.Model):
    id = models.AutoField(primary_key=True)
    # discussion -> default = ' ', null = True (추가)
    discussion = models.ForeignKey(Discussion, on_delete = models.CASCADE, related_name="comments", default='', null=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    content = models.TextField(blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)