from django.db import models
from django.contrib.auth.models import User


# Daily Record 글
class Discussion(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50)
    body = models.TextField(max_length=500)
    writer = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Discussion 카테고리
    category = models.CharField(max_length=50, null = False, blank = True)

# Daily Record 댓글
class DComment(models.Model):
    record = models.ForeignKey(Discussion, on_delete = models.CASCADE)
    content = models.TextField(blank = False, null = False)
    writer = models.ForeignKey(User, on_delete = models.CASCADE)