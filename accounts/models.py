from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.conf import settings

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
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
    nickname = models.CharField(max_length=20, unique=True )
    country = models.CharField(max_length=10, default='', null=False, blank=False)
    city = models.CharField(max_length=10, default='', null=False, blank=False)
    profile_img = models.ImageField(upload_to=image_upload_path, blank=True, null=True, default='default/default_profile_img.png')
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='friends', on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'country', 'city']

    objects = UserManager()

    def __str__(self):
        return self.email