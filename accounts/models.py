from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    # 일반 유저 생성
    def create_user(self, email, nickname, country, city, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not nickname:
            raise ValueError(_('The nickname must be set'))
        if not country:
            raise ValueError(_('The country must be set'))
        if not city:
            raise ValueError(_('The city must be set'))
        
        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname,
            country = country,
            city = city
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    username = None
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True, default='', null=False, blank=False)
    nickname = models.CharField(max_length=20, unique=True, )
    country = models.CharField(max_length=10, default='', null=False, blank=False)
    city = models.CharField(max_length=10, default='', null=False, blank=False)
    profile_img = models.ImageField(upload_to=image_upload_path, blank=True, null=True, default='default/default_profile_img.png')
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'country', 'city']

    objects = UserManager()

    def __str__(self):
        return self.email