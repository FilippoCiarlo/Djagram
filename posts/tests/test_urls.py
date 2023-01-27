from django.test import SimpleTestCase
from django.urls import reverse, resolve

# Views
from posts.views import post_list_view
from posts.views import post_detail_view
from posts.views import post_create_view
from posts.views import post_update_view
from posts.views import post_delete_view
from posts.views import like_view
from posts.views import search_view
from posts.views import profile_posts_view
from posts.views import homepage_view

class TestUrls(SimpleTestCase):
	
	def test_post_list_view_resolves(self):
		url = reverse("post_list")
		self.assertEqual(resolve(url).func, post_list_view)

	def test_post_list_by_tag_view_resolves(self):
		url = reverse("post_list_by_tag", args=["tag-slug"])
		self.assertEqual(resolve(url).func, post_list_view)

	def test_post_detail_view_resolves(self):
		url = reverse("post_detail", args=[1])
		self.assertEqual(resolve(url).func, post_detail_view)

	def test_post_create_view_resolves(self):
		url = reverse("new_post")
		self.assertEqual(resolve(url).func, post_create_view)

	def test_post_update_view_resolves(self):
		url = reverse("post_update",  args=[1])
		self.assertEqual(resolve(url).func, post_update_view)

	def test_post_delete_view_resolves(self):
		url = reverse("post_delete",  args=[1])
		self.assertEqual(resolve(url).func, post_delete_view)

	def test_like_view_resolves(self):
		url = reverse("like_post", args=[1])
		self.assertEqual(resolve(url).func, like_view)

	def test_search_view_resolves(self):
		url = reverse("search_results")
		self.assertEqual(resolve(url).func, search_view)

	def test_profile_posts_view_resolves(self):
		url = reverse("profile", args=["username"])
		self.assertEqual(resolve(url).func, profile_posts_view)

	def test_profile_posts_view_resolves(self):
		url = reverse("home")
		self.assertEqual(resolve(url).func, homepage_view)


