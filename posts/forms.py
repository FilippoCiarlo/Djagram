from django import forms

from .models import Post
from .models import Comment

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ['image','description','tags']


class CommentForm(forms.ModelForm):
	text = forms.CharField(required=False, label='')

	class Meta:
		model = Comment
		fields = ['text']
