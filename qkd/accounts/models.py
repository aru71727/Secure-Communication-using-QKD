from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class secret_keys(models.Model):
	sender_key = models.CharField(max_length=1000)
	receiver_key = models.CharField(max_length=1000)

class Profile(models.Model):
	
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	address = models.CharField(max_length=30)
	mobile = models.CharField(max_length=13)
	gender = models.CharField(max_length=6)
	joined_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)


	def __str__(self):
		return self.address

	def __unicode__(self):
		return self.address

class Messages(models.Model):
	sender = models.CharField(max_length=30)
	receiver = models.CharField(max_length=30)
	msg_body = models.CharField(max_length=250)
	seen = models.BooleanField(default=False)
	date_time = models.DateTimeField(auto_now=False,auto_now_add=True, null=True)
	

	def __str__(self):
		return self.msg_body[0:10]


