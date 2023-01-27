from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django import forms

from .models import Profile



# Forms
class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['image', 'bio']