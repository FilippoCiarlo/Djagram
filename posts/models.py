from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.urls import reverse

User = settings.AUTH_USER_MODEL


# Create your models here.
class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='images/', blank=False, null=False)
	description = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now_add=True)

	active = models.BooleanField(default=True)
	tags = TaggableManager()
	likes = models.ManyToManyField(User, related_name='likes')

	class Meta:
		ordering = ["-created"]
		indexes = [ models.Index(fields=['-created']), ]

	def total_likes(self):
		number_of_likes = int(self.likes.count())
		return number_of_likes

	def get_absolute_url(self):
		return reverse("post_detail", args=[str(self.id)])


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE) 
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now_add=True)

	active = models.BooleanField(default=True)

	class Meta:
		ordering = ['created']
		indexes = [ models.Index(fields=['created']), ]