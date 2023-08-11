from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


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
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag, blank=True)
    # 조회수
    views = models.PositiveSmallIntegerField(default=0)
    # 좋아요
    likes = models.PositiveSmallIntegerField(default=0)
    # 사진들을 저장할 ManyToMany 필드
    photos = models.ManyToManyField('Record_Photo', related_name='Record_Photo', blank=True)

# Record 사진
class Record_Photo(models.Model):
    image = models.ImageField(upload_to='record_photos/')


# Daily Record 댓글
class RComment(models.Model):
    record = models.ForeignKey(Record, on_delete = models.CASCADE)
    content = models.TextField(blank = False, null = False)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
