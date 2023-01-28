import os
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Models
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .models import Post
from .models import Comment

# Forms
from .forms import PostForm
from .forms import CommentForm



# Create your views here
def homepage_view(request):
	# retrieve all website posts
	posts = Post.objects.all()
	return render(request,"posts/homepage.html", context={"posts":posts})



@login_required
def profile_posts_view(request, username):
	# given a username of an existing user
	# retrieve all his posts
	user_profile = get_object_or_404(User, username=username)
	posts = Post.objects.filter(user=user_profile)

	context={
		"posts": posts,
		"user_profile": user_profile,
	}

	return render(request,"posts/profile_posts.html", context)



@login_required
def post_list_view(request, tag_slug=None):
	user = get_object_or_404(User, username=request.user.username)

	# retrieve the post of the user
	posts = Post.objects.filter(user=user)
	
	# retrieve the posts of the followed people
	for follow in user.profile.follows.all():
		posts |= Post.objects.filter(user=follow)

	# Post by Tag
	# given a tag retrive all the 
	# post with the given tag
	tag = None
	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		posts = posts.filter(tags__in=[tag])

	context={
		"posts": posts,
		"tag": tag
	}

	return render(request,"posts/post_list.html", context)


def post_detail_view(request, id):
	post = get_object_or_404(Post, id=id)
	user = request.user

	# Like System
	total_likes = post.total_likes()
	liked = False
	if post.likes.filter(id=user.id).exists():
		liked = True

	# List of similar posts
	# retrieve all the posts that have in their
	# tags list one or more tags of the given post
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=id) 
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]

	# Comment System
	comments = post.comments.filter(active=True)
	comment = Comment()
	comment_form = CommentForm()
	if request.method == "POST":
		# Check if the comment is an empty comment
		if len(request.POST.get("text")) == 0 : 
			messages.info(request, ("You have to write something to comment."))
		else:
			comment_form = CommentForm(request.POST)
			if comment_form.is_valid():
				comment = Comment(
					user=user,
					post=post,
					text=comment_form.cleaned_data['text']
				)
				comment.save()
				# Clean the form
				comment_form = CommentForm() 
			
	context = {
		"post": post, 
		'similar_posts': similar_posts, 
		'total_likes':total_likes, 
		'liked':liked,
		'comments':comments,
		'comment': comment,
		'comment_form':comment_form,
	}

	return render(request,"posts/post_detail.html", context)


@login_required
def post_create_view(request):
	form = PostForm()
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			img_obj = form.instance
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()
			form.save()
			form = PostForm()
			return HttpResponseRedirect(reverse('post_detail', args=[str(obj.id)]))

	return render(request, "posts/post_create.html", context={"form":form})


@login_required
def post_update_view(request, id):
	post = get_object_or_404(Post, id=id) 
	form = PostForm(instance=post)
	user = request.user

	# if the request's user is
	# the author of the post too
	if user == post.user:
		if request.method == 'POST':
			# Update Image
			if len(request.FILES) != 0:	
				# delete the old image
				image_path = post.image.path
				if os.path.exists(image_path):
					os.remove(image_path)
				# load the new image
				image = request.FILES.get('image')
				post.image = image

			# Update Description
			post.description = request.POST.get('description')

			# Update Tags
			new_tags = request.POST.get('tags')
			new_tags = list(new_tags.replace(" ", "").split(","))
			if len(new_tags) != 0:
				post.tags.set(new_tags, clear=True)
			
			post.save()
			messages.success(request, ("Post updated successfully."))
			return HttpResponseRedirect(reverse('post_detail', args=[str(id)]))
	else:
		return HttpResponseRedirect(reverse('post_detail', args=[str(id)]))

	context = {
		"form":form, 
		"post": post
	}
	
	return render(request, 'posts/post_update.html', context)


@login_required
def post_delete_view(request, id):
	post = get_object_or_404(Post, id=id) 
	user = request.user
	
	# if the request's user is
	# the author of the post too
	if user == post.user:
		if request.method == 'POST':
			# delete the post
			post_to_delete = post
			post_to_delete.delete()

			# delete the old post image
			image_path = post.image.path
			if os.path.exists(image_path):
				os.remove(image_path)
			
			messages.success(request, ("The Post it's been deleted successfully."))
			return redirect("post_list")
	else:
		return HttpResponseRedirect(reverse('post_detail', args=[str(id)]))

	return render(request, 'posts/post_delete.html', {'post':post})


@login_required
def like_view(request, id):
	post = get_object_or_404(Post, id=id)
	user = request.user

	# Like a post if it hasn't already been liked
	liked = False
	if post.likes.filter(id=user.id).exists():
		post.likes.remove(user)
		liked = False
	else:
		post.likes.add(user)
		liked = True

	return HttpResponseRedirect(reverse('post_detail', args=[str(id)]))


def search_view(request):
	query = request.GET.get('q')
	posts = None
	users = None
	tags = None

	# If the query is a valid query
	if query is not None:
		if len(str(query)) > 0:

			# retrieve all the post that match 
			# by description, tag or author
			posts = Post.objects.filter(
				Q(description__icontains=query) | 
				Q(user__username__icontains=query) |
				Q(tags__name__iexact=query)
			).distinct()
		
			# retrieve all the users and tags 
			# that match with the query
			users = User.objects.filter(username__icontains=query)
			tags = Tag.objects.filter(Q(name__icontains=query))

	context = {
		"users": users,
		"posts": posts,
		"tags": tags,
	}

	return render(request, "posts/search_results.html", context)



