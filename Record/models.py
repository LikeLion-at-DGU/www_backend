from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# 이미지 업로드 함수...?!
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'



# Card 태그
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


# Daily Record 글
class Record(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    weather = models.CharField(max_length=50)
    date = models.DateField(null = True, blank = True, default = None)
    body = models.TextField(max_length=2000)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 조회수
    views = models.PositiveSmallIntegerField(default=0)
    # 좋아요
    rlike = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='rlikes', blank=True)
    rlike_count = models.PositiveIntegerField(default=0)
    # 스크랩
    record_scrap = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='record_scraps', blank=True)
    
    #카드 관련 -------------------------------------------------------------------
    where = models.CharField(max_length=80)
    what = models.CharField(max_length=100)
    how = models.CharField(max_length=100)
    # Card 태그를 입력하는 창(?)
    tag_field = models.CharField(max_length=80, default=0, null=True)
    # Card 태그
    tag = models.ManyToManyField(Tag, blank=True)
    # Card 사진
    card_photo_1 = models.ImageField(upload_to=image_upload_path) # null = True 사진을 첨부 안해도 돌아가게 하는....그런...
    card_photo_2 = models.ImageField(upload_to=image_upload_path, blank = True, null = True)
    card_photo_3 = models.ImageField(upload_to=image_upload_path, blank = True, null = True)
    # Card 스크랩
    card_scrap = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='card_scraps', blank=True)



# Record 사진
class Record_Photo(models.Model):
    image = models.ImageField(upload_to=image_upload_path)


# Daily Record 댓글
class RComment(models.Model):
    record = models.ForeignKey(Record, on_delete = models.CASCADE, related_name = "rcomments")
    content = models.TextField(blank = False, null = False)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank=False, null=True)
    # RComment 좋아요
    rcomment_like = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='rcomment_likes', blank=True)
    rcomment_like_count = models.PositiveIntegerField(default=0)


# 이미지 URL 저장되는 모델
class Upload_image(models.Model):
    url = models.ImageField(upload_to=image_upload_path)