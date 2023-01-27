from django.test import TestCase, Client
from django.urls import reverse

# Models
from django.contrib.auth.models import User


class TestModels(TestCase):
	def setUp(self):
		self.client = Client()

		### Users ###
		self.user = User.objects.create_user(
			username='MarioRossi', 
			password='testpass123'
		)
		############


	# __str__ Method
	def test_profile_str_(self):
		self.assertEqual(str(self.user.profile), f"{ self.user.username } Profile")
