from django.db import models
import os
import uuid
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

class Alumni(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length = 200, null=True)
	phone = models.CharField(max_length = 200, null=True)
	email = models.CharField(max_length = 200, null=True)
	passing_year = models.IntegerField(null=True)
	enrollment_number = models.CharField(max_length=200, null = True)
	course = models.CharField(max_length=200, null = True)
	branch = models.CharField(max_length=200, null = True)
	current_state = models.CharField(max_length=200, null = True)
	current_city = models.CharField(max_length=200, null = True)
	current_job = models.CharField(max_length=200, null = True)
	profile_pic = models.ImageField(default = 'profile1.png', null=True, blank = True)
	date_created = models.DateTimeField(auto_now_add= True, null = True)
	
	def __str__(self):
		return str(self.user)

class Notice(models.Model):
	alumni = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)
	title = models.CharField(max_length=200, null = True)
	noticefile = models.FileField(upload_to='files/',null = True)
	def __str__(self):
		return str(self.title)
