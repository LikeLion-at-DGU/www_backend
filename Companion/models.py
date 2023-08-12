from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Companion(models.Model):
    # 글 field
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()
    date = models.DateField() 
    continent = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    # 그 외 field
    views = models.PositiveIntegerField(default=0)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='likes', blank=True)
    like_count = models.PositiveIntegerField(default=0)
    
    # 좋아요 방식 기존으로하자 

class CoComment(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    companion = models.ForeignKey(Companion, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='comment_likes', blank=True)
    like_count = models.PositiveIntegerField(default=0)
    