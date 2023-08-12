from django.contrib import admin
from .models import Discussion, DComment, Choice

# Register your models here.
admin.site.register(Discussion)
admin.site.register(DComment)
admin.site.register(Choice)