from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from posts.views import post_list_view
from posts.views import post_detail_view
from posts.views import post_create_view
from posts.views import post_update_view
from posts.views import post_delete_view
from posts.views import like_view
from posts.views import search_view
from posts.views import profile_posts_view

urlpatterns = [
    path('', post_list_view, name="post_list"), 
    path('tag/<slug:tag_slug>/',post_list_view, name="post_list_by_tag"),
    path('<int:id>/', post_detail_view, name="post_detail"),
    path('new/', post_create_view, name="new_post"),
    path('edit/<int:id>/', post_update_view, name="post_update"),
    path('delete/<int:id>/', post_delete_view, name="post_delete"),
    path('like/<int:id>/', like_view, name="like_post"),
    path("search/", search_view, name="search_results"),
    path('profile/<str:username>', profile_posts_view, name="profile"),
]