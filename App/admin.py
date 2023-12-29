from django.contrib import admin
from .models import Profile, Post, Likepost, Followers

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Likepost)
admin.site.register(Followers)
