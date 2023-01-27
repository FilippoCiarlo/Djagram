from django.contrib import admin

from .models import Post
from .models import Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('user','description','created', 'active')
	list_filter = ('active', 'created')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'text', 'created', 'active')
	list_filter = ('active', 'created')




