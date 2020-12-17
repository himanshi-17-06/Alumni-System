from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from .models import *

class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )
class AlumniForm(ModelForm):
	class Meta:
		model = Alumni
		fields = '__all__'
		exclude = ['user', 'email', 'name']

class NoticeForm(ModelForm):
	class Meta:
		model = Notice
		fields = ['title', 'noticefile']


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2']
