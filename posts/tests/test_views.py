from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.messages import get_messages

# Models
from django.contrib.auth.models import User
from posts.models import Post
from posts.models import Comment

# Image
from os.path import join
from django.core.files.uploadedfile import SimpleUploadedFile

# Tags
from taggit.managers import TaggableManager



class TestViews(TestCase):
	def setUp(self):
		self.client = Client()

		### Images ###
		self.image_path_1 = join("posts/tests/test_image.jpg")
		self.image_path_2 = join("posts/tests/test_image_2.jpg")
		self.image_1 = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path_1, 'rb').read(), content_type='image/jpeg')
		self.image_2 = SimpleUploadedFile(name='test_image_2.jpg', content=open(self.image_path_2, 'rb').read(), content_type='image/jpeg')
		##############

		### Users ###
		self.user = User.objects.create_user(
			username='MarioRossi', 
			password='testpass123'
		)
		self.user_not_owner = User.objects.create_user(
			username='NotPostOwner', 
			password='testpass456'
		)
		############

		### Post ###
		self.post = Post.objects.create(
			user=self.user,
			image = self.image_1,
			description="This is the description of a Post",
		)
		self.post.tags.add("Post-Tag", "MarTag")
		############

		### Urls ###
		self.post_list_url = reverse("post_list")
		self.post_list_by_tag_url = reverse("post_list_by_tag", args=["post-tag"])
		self.post_detail_url = reverse("post_detail", args=[1])
		self.post_create_url = reverse("new_post")
		self.post_update_url = reverse("post_update", args=[1])
		self.post_delete_url = reverse("post_delete", args=[1])
		self.post_like_url = reverse("like_post", args=[1])
		self.post_search_url = reverse("search_results")
		self.profile_url = reverse("profile", args=["MarioRossi"])
		self.homepage_url = reverse("home")
		############



	# Post List
	"""
		Verifica che i post mostrati all'interno della bacheca 
		di un utente registrato, che non segue nessun altro utente, 
		siano solato i suoi post.
	"""
	def test_post_list_view_NotFollows_Success(self):

		user2 = self.user_not_owner
		user2_post = Post.objects.create(
			user=user2,
			image = self.image_2,
			description="This is user2 Post description",
			tags=self.post.tags
		)
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.post_list_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/post_list.html")
		self.assertContains(response, str(self.post.description)) 
		self.assertNotContains(response, str(user2_post.description)) 


	"""
		Verifica che i post mostrati all'interno della bacheca 
		di un utente registarto, che segue un'altro utente, 
		siano i suoi post e quelli dell'utente seguito.
	"""
	def test_post_list_view_Follows_Success(self):
		user2 = self.user_not_owner
		self.user.profile.follows.add(user2)
		user2_post = Post.objects.create(
			user=user2,
			image = self.image_2,
			description="This is user2 Post description",
			tags=self.post.tags
		)
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.post_list_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/post_list.html")
		self.assertContains(response, str(self.post.description)) 
		self.assertContains(response, str(user2_post.description)) 


	"""
		Verifica che un utente non-registrato 
		non abbia accesso alla bacheca dei post.
	"""
	def test_post_list_view_Insuccess(self):
		response = self.client.get(self.post_list_url)
		self.assertRedirects(
			response, 
			"/accounts/login/?next=/posts/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)



	# Post List by Tag
	"""
		Verifica che un utente non-registrato abbia 
		accesso alla lista dei post aventi uno specifico tag.
	"""
	def test_post_list_by_tag_view_Success(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.post_list_by_tag_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/post_list.html")
		self.assertContains(response, str(self.post.tags.first())) 


	"""
		Verifica che un utente non-registrato non abbia 
		accesso alla lista dei post aventi uno specifico tag.
	"""
	def test_post_list_by_tag_view_Insuccess(self):
		response = self.client.get(reverse("post_list_by_tag", args=["non-existent-tag"]))
		self.assertRedirects(
			response, 
			"/accounts/login/?next=/posts/tag/non-existent-tag/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)


	"""
		Verifica che dato un tag non esistente 
		venga riornata la pagina di errore 404.
	"""
	def test_post_list_by_tag_view_404(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(reverse("post_list_by_tag", args=["non-existent-tag"]))
		self.assertEquals(response.status_code, 404)



	# Post Detail
	"""
		Verifica che dato un post venga 
		ritornata la sua vista in dettaglio.
	"""
	def test_post_detail_view_Success(self):
		response = self.client.get(self.post_detail_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/post_detail.html")
		self.assertContains(response, str(self.post.description)) 


	"""
		Verifica che dato un post non esistente 
		venga ritornata la pagina di errore 404.
	"""
	def test_post_detail_view_404(self):
		# 0 = non existent post-id
		response = self.client.get(reverse("post_detail", args=[0]))
		self.assertEquals(response.status_code, 404)


	"""
		Verifica che un utente registrato possa 
		lasciare un commento sotto un post.
	"""
	def test_post_detail_view_Success_LoggedIn_Comment_POST(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.post(self.post_detail_url,
			{
				"text":"This is a comment"
			}
		)
		self.assertEquals(response.status_code, 200)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 0)


	"""
		Verifica che un utente registrato non possa 
		lasciare un commento vuoto sotto un post.
	"""
	def test_post_detail_view_Insuccess_LoggedIn_Comment_POST(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.post(self.post_detail_url,
			{
				"text":""
			}
		)
		self.assertEquals(response.status_code, 200)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "You have to write something to comment.")



	# Post Create
	"""
		Verifica che un utente registrato abbia accesso 
		alla pagina di creazione di un nuovo post.
	"""
	def test_post_create_view_LoggedIn_Success(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.post_create_url)
		self.assertEquals(response.status_code, 200)
		
		# Test HTML code
		self.assertTemplateUsed(response, "posts/post_create.html")
		self.assertContains(response, "Create a new Post") 


	"""
		Verifica che un utente non-registrato non abbia 
		accesso alla pagina di creazione di un nuovo post.
	"""
	def test_post_create_view_LoggedOut_Insuccess(self):
		response = self.client.get(self.post_create_url)
		self.assertRedirects(
			response, 
			"/accounts/login/?next=/posts/new/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)


	"""
		Verifica che un utente registrato 
		possa creare un nuovo post.
	"""
	def test_post_create_view_Success_POST(self):
		image = self.image_2
		description = "This is the description for a New Post"
		tag = self.post.tags

		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.post(self.post_create_url, 
			{
				"image":image,
				"description":description,
				"tags":tag
			}
		)
		self.assertRedirects(
			response, 
			"/posts/2/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)
		self.assertEquals(Post.objects.all().count(), 2)



	# Post Update
	"""
		Verifica che un utente registrato abbia accesso 
		alla pagina di modifica di un proprio post.
	"""
	def test_post_update_view_LoggedIn_Success(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.post_update_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/post_update.html")
		self.assertContains(response, "Edit Post") 


	"""
		Verifica che un utente non-registrato non abbia
		accesso alla pagina di modifica di un post.
	"""
	def test_post_update_view_LoggedOut_Insuccess(self):
		response = self.client.get(self.post_update_url)
		self.assertRedirects(
			response, 
			"/accounts/login/?next=/posts/edit/1/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)


	"""
		Verifica che dato un post non esistente
		venga ritornata la pagina di errore 404.
	"""
	def test_post_update_view_404(self):
		# 0 = non existent post-id
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(reverse("post_update", args=[0]))
		self.assertEquals(response.status_code, 404)


	"""
		Verifica che un utente registrato 
		possa modificare un proprio post.
	"""
	def test_post_update_view_Success_POST(self):
		image = self.image_2
		description = "This is a New Description"
		tag = self.post.tags

		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.post(self.post_update_url, 
			{
				"image":image,
				"description":description,
				"tags":tag
			}
		)
		self.assertRedirects(
			response, 
			"/posts/1/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "Post updated successfully.")


	"""
		Verifica che un utente registrato non possa 
		modificare un post di un'altro utente.
	"""
	def test_post_update_view_Insuccess_POST(self):
		self.client.login(username='NotPostOwner', password='testpass456')
		response = self.client.post(self.post_update_url, 
			{
				"image":self.image_2,
				"description": "I'm not the owner of this post",
				"tags": self.post.tags
			}
		)
		self.assertRedirects(
			response, 
			"/posts/1/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 0)



	# Post Delete
	"""
		Verifica che un utente registrato abbia accesso
		alla pagina di cancellazione di un post.
	"""
	def test_post_delete_view_Success(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.post_delete_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/post_delete.html")
		self.assertContains(response, "Delete Post") 


	"""
		Verifica che un utente non-registrato non abbia 
		accesso alla pagina di cancellazione di un post.
	"""
	def test_post_update_view_Insuccess(self):
		response = self.client.get(self.post_delete_url)
		self.assertRedirects(
			response, 
			"/accounts/login/?next=/posts/delete/1/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)


	"""
		Verifica che dato un post non esistente
		venga ritornata la pagina di errore 404.
	"""
	def test_post_delete_view_404(self):
		# 0 = non existent post-id
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(reverse("post_delete", args=[0]))
		self.assertEquals(response.status_code, 404)


	"""
		Verifica che un utente registrato 
		possa cancellare un proprio post.
	"""
	def test_post_delete_view_Success_POST(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.post(self.post_delete_url)
		self.assertRedirects(
			response, 
			"/posts/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)
		self.assertEquals(Post.objects.all().count(), 0)
		
		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 1)
		self.assertEqual(str(messages[0]), "The Post it's been deleted successfully.")	


	"""
		Verifica che un utente registrato non possa
		cancellare un post di un'altro utente.
	"""
	def test_post_delete_view_Insuccess_POST(self):
		self.client.login(username='NotPostOwner', password='testpass456')
		response = self.client.post(self.post_delete_url)
		self.assertRedirects(
			response, 
			"/posts/1/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		# test website messages
		messages = list(get_messages(response.wsgi_request))
		self.assertEqual(len(messages), 0)



	# Like 
	"""
		Verifica che un utente non-registrato non abbia
		accesso alla funzionalita Like.
	"""
	def test_post_like_view_LoggedOut_Insuccess(self):
		response = self.client.get(self.post_like_url)
		self.assertRedirects(
			response, 
			"/accounts/login/?next=/posts/like/1/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)


	"""
		Verifica che dato un post non esistente
		venga ritornata la pagina di errore 404.
	"""
	def test_post_like_view_404(self):
		# 0 = non existent post-id
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(reverse("like_post", args=[0]))
		self.assertEquals(response.status_code, 404)


	"""
		Verifica che un utente registrato possa 
		mettere like ad un post.
	"""
	def test_post_like_view_Success_Like_POST(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.post_like_url)
		self.assertRedirects(
			response, 
			"/posts/1/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)
		self.assertTrue(self.post.likes.count() == 1)


	"""
		Verifica che un utente registrato possa 
		togliere like ad un post.
	"""
	def test_post_like_view_Success_Unlike_POST(self):
		self.client.login(username='MarioRossi', password='testpass123')
		self.client.get(self.post_like_url)
		response = self.client.get(self.post_like_url)
		self.assertRedirects(
			response, 
			"/posts/1/", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)

		self.assertTrue(self.post.likes.count() == 0)



	# Search
	"""
		Verifica che dato un database adeguatemente popolato per il test
		la ricerca vada a buon fine e ritorni un Username ed un Tag che 
		soddisfino la query.
	"""
	def test_post_search_view_Success(self):
		self.client.login(username='MarioRossi', password='testpass123')
		post_search_url = '{url}?{filter}={value}'.format(url=reverse("search_results"),filter="q", value="Mar")
		response = self.client.get(post_search_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/search_results.html")
		self.assertContains(response, "Search Results") 
		self.assertContains(response, "MarioRossi") 
		self.assertContains(response, "MarTag") 
		self.assertNotContains(response, "No Posts found.") 


	"""
		Verifica un utente non registarto riceva come
		risultato della ricerca solo post.
	"""
	def test_post_search_LoggedOut_view_Success(self):
		response = self.client.get(self.post_search_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/search_results.html")
		self.assertNotContains(response, "Users") 
		self.assertNotContains(response, "Tags") 
		self.assertContains(response, "Posts") 


	"""
		Verifica un utente registarto riceva come
		risultato della ricerca Utenti, Tag e Post.
	"""
	def test_post_search_LoggedIn_view_Success(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.post_search_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/search_results.html")
		self.assertContains(response, "Users") 
		self.assertContains(response, "Tags") 
		self.assertContains(response, "Posts") 



	# Profile
	"""
		Verifica un utente registarto abbia accesso
		alla vista del profilo di un utente.
	"""
	def test_profile_view_Success(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.profile_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/profile_posts.html")
		self.assertContains(response, "@MarioRossi") 
		self.assertNotContains(response, "MarioRossi hasn't posted anything yet.") 


	"""
		Verifica un utente non-registarto non abbia 
		accesso alla vista del profilo di un utente.
	"""
	def test_profile_view_Insuccess(self):
		response = self.client.get(self.profile_url)
		self.assertRedirects(
			response, 
			"/accounts/login/?next=/posts/profile/MarioRossi", 
			status_code=302, 
			target_status_code=200, 
			fetch_redirect_response=True
		)


	"""
		Verifica che dato un utente non esistente
		venga ritornata la pagine di errore 404.
	"""
	def test_profile_view_404(self):
		# Not-Existent-User = non existent/registered user
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(reverse("profile", args=["Not-Existent-User"]))
		self.assertEquals(response.status_code, 404)



	# Home
	"""
		Verifica che dato un utente non-registrato
		visualizzi la home page in modo corretto
	"""
	def test_home_view_LoggedOut_Success(self):
		response = self.client.get(self.homepage_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/homepage.html")
		self.assertContains(response, "Take a look to the latest Posts") 
		self.assertNotContains(response, "Hi MarioRossi!")


	"""
		Verifica che dato un utente registrato
		visualizzi la home page in modo corretto
	"""
	def test_home_view_LoggedIn_Success(self):
		self.client.login(username='MarioRossi', password='testpass123')
		response = self.client.get(self.homepage_url)
		self.assertEquals(response.status_code, 200)

		# Test HTML code
		self.assertTemplateUsed(response, "posts/homepage.html")
		self.assertContains(response, "Take a look to the latest") 
		self.assertContains(response, "Hi MarioRossi!")


