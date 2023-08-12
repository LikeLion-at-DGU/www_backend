from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Card 태그
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
    record = models.ForeignKey(Record, on_delete = models.CASCADE, related_name = "rcomments")
    content = models.TextField(blank = False, null = False)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)


# Card 모델
class Card(models.Model):
    id = models.AutoField(primary_key=True)
    record = models.ForeignKey(Record, on_delete = models.CASCADE, related_name = "cards") # Record 글과 ForeignKey 연결
    where = models.CharField(max_length=80)
    what = models.CharField(max_length=100)
    how = models.CharField(max_length=100)
    # Card 태그를 입력하는 창(?)
    tag_field = models.CharField(max_length=80, default=0, null=True)
    # Card 태그
    tag = models.ManyToManyField(Tag, blank=True)
    # Card 사진
    card_photo_1 = models.ImageField(upload_to='record_photos/', null = True) # null = True 사진을 첨부 안해도 돌아가게 하는....그런...
    card_photo_2 = models.ImageField(upload_to='record_photos/', null = True)
    card_photo_3 = models.ImageField(upload_to='record_photos/', null = True)