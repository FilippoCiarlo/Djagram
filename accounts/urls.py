from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('login/', views.login_view, name="login"),
	path('logout/', views.logout_view, name="logout"),
	path('signup/', views.signup_view, name="signup"),
	path('profile/edit', views.edit_profile_view, name="edit_profile"),
	path('profile/edit/delete', views.delete_profile_view, name="delete_profile"),
	path('profile/<str:username>/follow', views.follow_view, name="follow"),
	path(
		'password-reset/', 
		auth_views.PasswordResetView.as_view(template_name="accounts/reset/password_reset.html"), 
		name="password_reset"
	),
	path(
		'password_reset/done/', 
		auth_views.PasswordResetDoneView.as_view(template_name="accounts/reset/password_reset_done.html"), 
		name="password_reset_done"
	),
	path(
		'reset/<uidb64>/<token>/', 
		auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset/password-reset-confirm.html"), 
		name="password_reset_confirm"
	),	
	path(
		'reset/done/', 
		auth_views.PasswordResetCompleteView.as_view(template_name="accounts/reset/password_reset_complete.html"), 
		name="password_reset_complete"
	),
]