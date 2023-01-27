from django.test import SimpleTestCase
from django.urls import reverse, resolve


from accounts.views import login_view
from accounts.views import logout_view
from accounts.views import signup_view
from accounts.views import edit_profile_view
from accounts.views import delete_profile_view
from accounts.views import follow_view


from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView



class TestUrls(SimpleTestCase):

	def test_login_view_resolves(self):
		url = reverse("login")
		self.assertEqual(resolve(url).func, login_view)

	def test_logout_view_resolves(self):
		url = reverse("logout")
		self.assertEqual(resolve(url).func, logout_view)

	def test_signup_view_resolves(self):
		url = reverse("signup")
		self.assertEqual(resolve(url).func, signup_view)

	def test_edit_profile_view_resolves(self):
		url = reverse("edit_profile")
		self.assertEqual(resolve(url).func, edit_profile_view)

	def test_delete_profile_view_resolves(self):
		url = reverse("delete_profile")
		self.assertEqual(resolve(url).func, delete_profile_view)

	def test_delete_profile_view_resolves(self):
		url = reverse("follow", args=["username"])
		self.assertEqual(resolve(url).func, follow_view)