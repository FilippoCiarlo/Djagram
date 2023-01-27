from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import login

# Models
from django.contrib.auth.models import User
from posts.models import Post
from posts.models import Comment

# Image
from os.path import join
from django.core.files.uploadedfile import SimpleUploadedFile

# Tags
from taggit.managers import TaggableManager



class TestModels(TestCase):
	def setUp(self):
		self.client = Client()

		### Users ###
		self.user = User.objects.create_user(
			username='MarioRossi', 
			password='testpass123'
		)
		############

		### Images ###
		self.image_path_1 = join("posts/tests/test_image.jpg")
		self.image_1 = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path_1, 'rb').read(), content_type='image/jpeg')
		##############

		### Post ###
		self.post = Post.objects.create(
			user= self.user,
			image = self.image_1,
		)
		self.post.tags.add("Post-Tag", "MarTag")
		############

	"""
	def test_total_likes(self):
		# Number of likes when the post is created
		self.assertEqual(int(self.post.total_likes), 0)

		# Number of likes after a user left a Like
		self.client.login(username='MarioRossi', password='testpass123')
		self.client.get(reverse("like_post", args=[1]))
		self.assertEqual(int(self.post.total_likes), 1)


	def test_get_absolute_url(self):
		url = reverse("post_detail", args=[1])
		self.assertEqual(str(self.post.get_absolute_url), url)
	"""




