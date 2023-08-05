from django.db import models
from django.contrib.auth.models import User


# Daily Record 태그
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

# Daily Record 글
class Record(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    weather = models.CharField(max_length=50)
    body = models.TextField(max_length=200)
    writer = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag, blank=True)

# Daily Record 댓글
class RComment(models.Model):
    record = models.ForeignKey(Record, on_delete = models.CASCADE)
    content = models.TextField(blank = False, null = False)
    writer = models.ForeignKey(User, on_delete = models.CASCADE)
