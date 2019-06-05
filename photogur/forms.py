from django.forms import Form, CharField, PasswordInput, ModelForm
from .models import Picture, Comment

class LoginForm(Form):
	username = CharField(label="User Name", max_length=64)
	password = CharField(widget=PasswordInput())

class PictureForm(ModelForm):
	class Meta:
		model = Picture
		fields = ['title', 'artist', 'url']

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['message', 'name']
