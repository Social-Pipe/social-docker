from django.contrib import admin
from app.posts.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
