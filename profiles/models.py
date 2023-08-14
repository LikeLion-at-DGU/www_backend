from django.db import models
from django.conf import settings

def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    country = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    profile_img = models.ImageField(upload_to=image_upload_path, blank=True, null=True, default='default/default_profile_img.png')
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def __str__(self) -> str:
        return self.nickname