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
	posts = Post.objects.all()

	context = {
		"posts":posts,
	}

	return render(request,"posts/homepage.html", context)


@login_required
def profile_posts_view(request, username):
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
	posts = Post.objects.filter(user=user)
	
	for follow in user.profile.follows.all():
		posts |= Post.objects.filter(user=follow)

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
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=id) 
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]

	# Comment System
	comments = post.comments.filter(active=True)
	comment = Comment()
	comment_form = CommentForm()
	if request.method == "POST":
		if len(request.POST.get("text")) == 0 : # Check if the comment is an empty comment
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
				comment_form = CommentForm() # Clean the form
			
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

	context = {
		"form":form
	}

	return render(request, "posts/post_create.html", context)


@login_required
def post_update_view(request, id):
	post = get_object_or_404(Post, id=id) 
	form = PostForm(instance=post)
	user = request.user

	if user == post.user:
		if request.method == 'POST':
			# Update Image
			if len(request.FILES) != 0:	
				image_path = post.image.path
				if os.path.exists(image_path):
					os.remove(image_path)
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
	
	if user == post.user:
		if request.method == 'POST':
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

	#if query is not None & 
	#query = None
	#print("HERE:",query,type(query),len(query))

	if query is not None:
		if len(str(query)) > 0:
			posts = Post.objects.filter(
				Q(description__icontains=query) | 
				Q(user__username__icontains=query) |
				Q(tags__name__iexact=query)
			).distinct()
		
			users = User.objects.filter(username__icontains=query)
			tags = Tag.objects.filter(Q(name__icontains=query))

	context = {
		"users": users,
		"posts": posts,
		"tags": tags,
	}

	return render(request, "posts/search_results.html", context)



