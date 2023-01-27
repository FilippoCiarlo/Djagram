from django.contrib.auth import get_user_model, get_user, login
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse, resolve



# Models
from .models import Profile

# Forms
from .forms import UserRegisterForm
from .forms import UserUpdateForm
from .forms import ProfileUpdateForm

# Views
from .views import signup_view
from .views import login_view
from .views import logout_view



# Create your tests here.
class UserTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='MarioRossi', 
			first_name="Mario",
			last_name="Rossi",
			email="mariorossi@email.com", 
			password='testpass123'
		)

	def test_create_user(self):
		self.assertEqual(self.user.username, "MarioRossi") 
		self.assertEqual(self.user.email, "mariorossi@email.com") 
		self.assertEqual(self.user.first_name, "Mario")
		self.assertEqual(self.user.last_name, "Rossi")
		self.assertEqual(self.user.profile.image, "default.jpg")
		self.assertEqual(self.user.profile.bio, "This is my bio.")
		self.assertEqual(self.user.profile.__str__(), "MarioRossi Profile")
		self.assertTrue(self.user.is_active) 
		self.assertFalse(self.user.is_staff) 
		self.assertFalse(self.user.is_superuser)


	def test_profile_created_via_signal(self):
		qs = Profile.objects.all()
		self.assertEqual(qs.count(), 1)


	def test_create_superuser(self):
		admin_user = User.objects.create_superuser(
			username="admin", 
			email="admin@email.com", 
			password="testpass345"
		)


		self.assertEqual(admin_user.username, "admin") 
		self.assertEqual(admin_user.email, "admin@email.com") 
		self.assertTrue(admin_user.is_active) 
		self.assertTrue(admin_user.is_staff) 
		self.assertTrue(admin_user.is_superuser)


class SignUpPageTests(TestCase):
	def setUp(self):
		self.signup_url = reverse("signup") 
		self.user = {
			'username': "buzzlightyear",
			'first_name': "buzz",
			'last_name': "lightyear",
			'email': "buzz@email.com",
			'password1': "testpass678",
			'password2': "testpass678",
		}

		self.user_with_taken_email = {
			'username': "buzz",
			'email': "buzz@email.com",
		}
		return super().setUp()

	def test_signup_template(self):
		response = self.client.get(self.signup_url)
		self.assertEqual(response.status_code, 200) 
		self.assertTemplateUsed(response, "accounts/authenticate/signup.html") 
		self.assertContains(response, "Signup") 
		self.assertNotContains(response, "Non dovrei essere su questa pagina.")

	def test_signup_view(self):
		view = resolve("/accounts/signup/") 
		self.assertEqual(view.func.__name__, signup_view.__name__)

	def test_signup_form(self):
		response = self.client.post(path=self.signup_url, data=self.user, format="text/html")
		self.assertEqual(response.status_code, 302)
		self.assertEqual(User.objects.all().count(), 1) 
		self.assertEqual(User.objects.all()[0].username, self.user['username']) 
		self.assertEqual(User.objects.all()[0].email, self.user['email'])

		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "Your account it's been created successfully.")


	def test_signup_form_email_already_taken(self):
		old_user = User.objects.create_user(
			self.user_with_taken_email['username'], 
			self.user_with_taken_email['email']
		)
		response = self.client.post(path=self.signup_url, data=self.user, format="text/html")
		self.assertEqual(response.status_code, 302)

		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "This email is already in use by another user.")



class LoginPageTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.login_url = reverse("login")

		self.credentials = {
			'username': 'MarioRossi',
			'password': 'testpass123'
		}

		self.wrong_credentials = {
			'username': 'MarioRossi',
			'password': 'wrong_password'
		}

		User.objects.create_user(**self.credentials)

	### LOGIN ###
	def test_login_template(self):
		response = self.client.get(self.login_url)
		self.assertEqual(response.status_code, 200) 
		self.assertTemplateUsed(response, "accounts/authenticate/login.html") 
		self.assertContains(response, "Login") 
		self.assertNotContains(response, "Non dovrei essere su questa pagina.")


	def test_login_view(self):
		view = resolve("/accounts/login/") 
		self.assertEqual(view.func.__name__, login_view.__name__)


	def test_login_success(self):
		response = self.client.post(self.login_url, self.credentials)      	
		#self.assertRedirects(response, "/posts/", status_code=302, target_status_code=200, fetch_redirect_response=True)


		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 0)


	def test_login_insuccess(self):
		response = self.client.post(self.login_url, self.wrong_credentials)      	
		self.assertRedirects(response, "/accounts/login/", status_code=302, target_status_code=200, fetch_redirect_response=True)

		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "There was an error logging in, try again.")


































