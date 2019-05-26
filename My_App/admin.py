from django.contrib import admin

from .models import  User, ImageUpload

#admin.site.register(Users)
admin.site.register(User)
admin.site.register(ImageUpload)

# Register your models here.
