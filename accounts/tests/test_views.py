from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.messages import get_messages

# Models
from django.contrib.auth.models import User
from accounts.models import Profile
from posts.models import Post

# Image
from os.path import join
from django.core.files.uploadedfile import SimpleUploadedFile

# Tags
from taggit.managers import TaggableManager



class TestViews(TestCase):
	def setUp(self):
		self.client = Client()

		### Images ###
		self.image_path_1 = join("accounts/tests/test_image.jpg")
		self.image_path_2 = join("accounts/tests/test_image_2.jpg")
		self.image_1 = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path_1, 'rb').read(), content_type='image/jpg')
		self.image_2 = SimpleUploadedFile(name='test_image_2.jpg', content=open(self.image_path_2, 'rb').read(), content_type='image/jpg')
		##############

		### Users ###
		self.user = User.objects.create_user(
			username ='MarioRossi',
			email ='mariorossi@email.com',
			password ='testpass123'
		)
		self.user.profile.image = self.image_1
		self.user.profile.bio = "This is my bio."

		self.user2 = User.objects.create_user(
			username ='ValentinoRossi',
			email ='valentinorossirossi@email.com',
			password ='testpass345'
		)
		############

		### Post ###
		self.post = Post.objects.create(
			user = self.user,
			image = self.image_1,
			description = "This is the description of a Post",
		)
		self.post.tags.add("Post-Tag", "MarTag")
		############

		### Urls ###
		self.accounts_login_url = reverse("login")
		self.accounts_logout_url = reverse("logout")
		self.accounts_signup_url = reverse("signup")
		self.accounts_follow_url = reverse("follow", args=["ValentinoRossi"])
		self.accounts_edit_profile_url = reverse("edit_profile")
		self.accounts_delete_profile_url = reverse("delete_profile")
		############



	# Login
	"""
		Verifica che un utente non-loggato
		abbia accesso alla pagina di login.
	"""
	def test_login_LoggedOut_view_Success(self):
		response = self.client.get(self.accounts_login_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "accounts/authenticate/login.html")
		self.assertContains(response, "Login") 


	"""
		Verifica che un utente gia' loggato
		non abbia accesso alla pagina di login.
	"""
	def test_login_LoggedIn_view_Inuccess(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.accounts_login_url)
		self.assertRedirects(
			response, 
			"/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)


	"""
		Verifica che il login di un utente registrato
		vada a buon fine e che questo venga reindirizzato
		alla bacheca dei post.
	"""
	def test_login_view_Success_POST(self):
		# Correct Credentials
		response = self.client.post(self.accounts_login_url,
			{
				"username": "MarioRossi",
				"password": "testpass123"
			}
		)
		self.assertRedirects(
			response, 
			"/posts/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)


	"""
		Verifica che il login di un utente con
		credenziali errate non vada a buon fine.
	"""
	def test_login_view_Insuccess_POST(self):
		# Incorrect Credentials
		response = self.client.post(self.accounts_login_url,
			{
				"username": "MarioRossi",
				"password": "wrongPassword"
			}
		)
		self.assertRedirects(
			response, 
			"/accounts/login/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "There was an error logging in, try again.")	



	# Logout
	"""
		Verifica che un utente gia loggato
		abbia accesso alla pagina di logout.
	"""
	def test_logout_LoggedIn_view_Success(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.accounts_logout_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "accounts/authenticate/logout.html")
		self.assertContains(response, "Logout") 


	"""
		Verifica che un utente non loggato
		non abbia accesso alla pagina di logout.
	"""
	def test_logout_LoggedOut_view_Insuccess(self):
		response = self.client.get(self.accounts_logout_url)
		self.assertRedirects(
			response, 
			"/accounts/login/?next=/accounts/logout/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)


	"""
		Verifica che il logout di un utente loggato
		vada a buon fine e che questo venga reindirizzato
		alla pagina di login.
	"""
	def test_logout_LoggedIn_view_Success_POST(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.post(self.accounts_logout_url)
		self.assertRedirects(
			response, 
			"/accounts/login/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "You were logged out successfully.")	



	# Signup
	"""
		Verifica che un utente non-loggato
		abbia accesso alla pagina di registrazione.
	"""
	def test_signup_LoggedOut_view_Success(self):
		response = self.client.get(self.accounts_signup_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "accounts/authenticate/signup.html")
		self.assertContains(response, "Signup") 


	"""
		Verifica che un utente loggato non abbia 
		accesso alla pagina di registrazione.
	"""
	def test_signup_LoggedIn_view_Insuccess(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.accounts_signup_url)
		self.assertRedirects(
			response, 
			"/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "You are already signed up.")	


	"""
		Verifica che la registrazione di un utente
		non-loggato e non precedentemente-registrato
		vada a buon fine e che questo venga reindirizzato
		alla bacheca dei post.
	"""
	def test_signup_view_Success_POST(self):
		response = self.client.post(self.accounts_signup_url,
			{
				"username": "JohnDoe",
				"first_name": "John",
				"last_name": "Doe",
				"email": "johndoe@email.com",
				"password1": "testpass345",
				"password2": "testpass345",
			}
		)
		self.assertRedirects(
			response, 
			"/posts/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "Your account it's been created successfully.")	


	"""
		Verifica che la registrazione di un utente
		non-loggato ma precedentemente-registrato
		non vada a buon fine e che questo venga 
		reindirizzato alla pagina di registrazione.
	"""
	def test_signup_view_Insuccess_POST(self):
		response = self.client.post(self.accounts_signup_url,
			{
				"username": "MarioRossino",
				"first_name": "Mario",
				"last_name": "Rossino",
				"email": "mariorossi@email.com",
				"password1": "testpass678",
				"password2": "testpass678",
			}
		)
		self.assertRedirects(
			response, 
			"/accounts/signup/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "This email is already in use by another user.")



	# Follow
	"""
		Verifica che un utente registrato possa 
		seguire (Follow) un'altro utente.
	"""
	def test_follow_profile_LoggedIn_view_Success_Follow_POST(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.post(self.accounts_follow_url)
		self.assertRedirects(
			response, 
			f"/posts/profile/{ self.user2.username }", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)
		self.assertEqual(self.user.profile.follows.count(),1)


	"""
		Verifica che un utente registrato possa smettere
		di seguire (Unfollow) un'altro utente.
	"""
	def test_follow_profile_LoggedIn_view_Success_Unollow_POST(self):
		self.client.login(username='MarioRossi', password='testpass123')
		self.client.post(self.accounts_follow_url)
		response = self.client.post(self.accounts_follow_url)
		self.assertRedirects(
			response, 
			f"/posts/profile/{ self.user2.username }", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		self.assertEqual(self.user.profile.follows.count(),0)



	# Edit Profile
	"""
		Verifica che un utente registrato abbia accesso
		alla pagina di modifica delle proprie impostazioni.
	"""
	def test_edit_profile_LoggedIn_view_Success(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.accounts_edit_profile_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "accounts/edit_profile.html")
		self.assertContains(response, "MarioRossi") 
		self.assertContains(response, "Profile Info") 


	"""
		Verifica che un utente non-registrato abbia accesso
		alla pagina di modifica delle impostazioni utente
	"""
	def test_edit_profile_LoggedOut_view_Insuccess(self):
		response = self.client.get(self.accounts_edit_profile_url)
		self.assertRedirects(
			response, 
			"/accounts/login/?next=/accounts/profile/edit", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)


	"""
		Verifica che un utente registarto possa modificare
		le proprie impostazioni.
	"""
	def test_edit_profile_view_Success_POST(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.post(self.accounts_edit_profile_url,
			{
				"username": "NewMarioRossi",
				"email": "newmariorossi@email.com",
				"image": self.image_2,
				"bio": "This is the New Mario Rossi bio.",
			}
		)
		self.assertRedirects(
			response, 
			"/accounts/profile/edit", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "Your profile was updated successfully.")



	# Delete Profile
	"""
		Verifica che un utente registrato abbia accesso
		alla pagina di cancellazione del proprio account.
	"""
	def test_delete_profile_LoggedIn_view_Success(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.accounts_delete_profile_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "accounts/delete_profile.html")
		self.assertContains(response, "Delete Account") 


	"""
		Verifica che un utente non-registrato non abbia 
		accesso alla pagina di cancellazione dell'account.
	"""
	def test_delete_profile_LoggedOut_view_Insuccess(self):
		response = self.client.get(self.accounts_delete_profile_url)
		self.assertRedirects(
			response, 
			"/accounts/login/?next=/accounts/profile/edit/delete", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)


	"""
		Verifica che un utente registrato possa
		cancellare il proprio account.
	"""
	def test_delete_profile_view_Success_POST(self):
		username = self.user.username
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.post(self.accounts_delete_profile_url)

		self.assertRedirects(
			response, 
			"/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), f"The user @{ username } is been deleted successfully.")







