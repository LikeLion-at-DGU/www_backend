from django.db import models
from django.contrib.auth.models import User


# Daily Record 글
class Discussion(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 투표 항목
class Choice(models.Model):
    # 여기 이제 discussion 하고 일대다 연결 필드 -> comment 보고 결정 이름
    vote_item = models.CharField(max_length=30)
    count = models.IntegerField(default=0)

# Discussion 댓글
class Comment(models.Model):
    record = models.ForeignKey(Discussion, on_delete = models.CASCADE)
    content = models.TextField(blank = False, null = False)
    writer = models.ForeignKey(User, on_delete = models.CASCADE)