

from os.path import join, split, exists


from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from django.test import TestCase
from django.urls import reverse

from social import settings




# Models
from .models import Post
from .models import Comment


# Create your tests here.
class PostTestCase(TestCase):

	def setUp(self):
		self.post_list_url = reverse("post_list")
		#self.post_detail_url = reverse("post_detail")

		self.image_path = join(settings.BASE_DIR, "media/test/test_image.jpg")

		self.user = User.objects.create_user(
			username='MarioRossi', 
			first_name="Mario",
			last_name="Rossi",
			email="mariorossi@email.com", 
			password='testpass123'
		)

		self.post = Post.objects.create(
			user=self.user,
			image = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(), content_type='image/jpeg'),
			description="This is a description",
		)

		self.comment = Comment.objects.create( 
			user=self.user,
			post=self.post,
			text = "This is a comment"
		)
 

	def test_post_list_view(self):
		# HERE LIST VIEW


	def test_post_detail_view(self):
		# HERE DETAIL VIEW











