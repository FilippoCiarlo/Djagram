import os
from social import settings

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm	
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Models
from .models import Profile
from posts.models import Post

# Forms
from .forms import UserRegisterForm  
from .forms import UserUpdateForm
from .forms import ProfileUpdateForm



# Create your views here.
def signup_view(request):
	# check if a logged-in-registered user try to signup
	# while he is already registered and logged-in
	if request.user.is_authenticated:
		messages.info(request, ("You are already signed up."))
		return redirect("home")

	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			# check if the email used to register
			# is already taken by another user
			email = form.cleaned_data['email']
			if User.objects.filter(email=email).exists():
				form = UserRegisterForm()
				messages.info(request, ("This email is already in use by another user."))
				return redirect("signup")

			form.save()

			# retrieve username and password
			# from the form to authenticate
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(
				request,
				username=username, 
				password=password
			)
			login(request,user)
			messages.success(request, ("Your account it's been created successfully."))
			return redirect("post_list")
	else:
		# clean the form
		form = UserRegisterForm()

	return render(request, "accounts/authenticate/signup.html", context={"form": form})



def login_view(request):
	# if a logged-in user try to login
	# while he is already logged-in
	if request.user.is_authenticated:
		return redirect("home")

	if request.method == "POST":
		# retrieve username and password
		# from the request to authenticate
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(
			request, 
			username=username, 
			password=password
		)

		if user is not None:
			# success login
			login(request, user)
			return redirect("post_list")
		else:
			# unsuccess login
			messages.info(request, ("There was an error logging in, try again."))
			return redirect("login")

	return render(request, "accounts/authenticate/login.html", {})



@login_required
def logout_view(request):
	if request.method == "POST":
		# success logout
		logout(request)
		messages.success(request, ("You were logged out successfully."))
		return redirect("login")
    
	return render(request, "accounts/authenticate/logout.html", {})



@login_required
def edit_profile_view(request):
	user = request.user
	if request.method == "POST":
		user_form = UserUpdateForm(request.POST, instance=user)
		
		# check if the email is already taken by another user
		email = request.POST['email']
		if User.objects.filter(email=email).exists():
			form = UserRegisterForm()
			messages.info(request, ("This email is already in use by another user."))
			return redirect("edit_profile")

		# delete the old user's profile image
		# if is not the defualt user image
		if len(request.FILES) != 0:	
			image_path = str(settings.BASE_DIR) + str(user.profile.image.url)				
			if os.path.exists(image_path):
				if "default.jpg" not in image_path:
					os.remove(image_path)

		# if the form is valid update the user's profile
		profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
		if user_form.is_valid and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, ("Your profile was updated successfully."))
			return redirect("edit_profile")
	else:
		# retrieve the user's data 
		user_form = UserUpdateForm(instance=user)
		profile_form = ProfileUpdateForm(instance=user.profile)		

	context = {
		"user_form":user_form,
		"profile_form":profile_form,
	}
	return render(request, "accounts/edit_profile.html", context)
	


def follow_view(request, username):
	# retrieve the user that we want to follow
	profile = get_object_or_404(User, username=username)

	if request.method == "POST":
		# retrieve the profile attached to the request's user
		current_user_profile = get_object_or_404(Profile, user=request.user)

		# if the request's user already follow the profile
		# remove it from the follow list otherwise add it
		if profile in current_user_profile.follows.all():
			current_user_profile.follows.remove(profile)		
		else:
			current_user_profile.follows.add(profile)

	return HttpResponseRedirect(reverse("profile", args=[str(profile.username)]))



@login_required
def delete_profile_view(request):
	username = request.user.username
	user = get_object_or_404(User, username=username)
	posts = Post.objects.filter(user=user)

	if request.method == "POST":
		# delete the user's posts images
		for post in posts:
			image_path = post.image.path
			if os.path.exists(image_path):
				os.remove(image_path)

		# delete the user's profile image
		# if is not the defualt user image
		image_path = str(settings.BASE_DIR) + str(user.profile.image.url)
		if os.path.exists(image_path):
			if "default.jpg" not in image_path:
				os.remove(image_path)

		# delete the user
		user.delete()

		# success feedback message
		messages.success(request, (f"The user @{ username } is been deleted successfully."))
		return redirect("home")

	return render(request, "accounts/delete_profile.html")

