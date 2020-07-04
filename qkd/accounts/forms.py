from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms
from .models import Profile

GENDER_CHOICES = [('Male','Male'), ('Female','Female'), ('Others','Others')]

class RegistrationForm(forms.Form):

	first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'autofocus':'on', 'autocomplete':'off', 'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Surname'}))
	# reg = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Registration Number'}))
	#dob = forms.DateField(label="Date of birth", widget=forms.DateInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'YYYY-MM-DD'}))
	#gender = forms.CharField(label='Gender', widget=forms.RadioSelect(choices=GENDER_CHOICES, attrs={'class':'custom-control-inline'}))
	gender= forms.CharField(label='Gender', widget=forms.Select(choices=GENDER_CHOICES))
	address = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'address'}))
	# college= forms.CharField(label='College', widget=forms.Select(choices=COLLEGE_CHOICES))
	mobile = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Mobile Number'}))
	email = forms.CharField(label="", widget=forms.EmailInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Email address'}))
	username = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Username'}))
	password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Your Password'}))
	cpassword = forms.CharField(label="", widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Confirm Password'}))
	
	def clean_email(self):
		email = self.cleaned_data.get("email")
		if len(User.objects.filter(email=email)):
			raise forms.ValidationError("Email Already Registered")

		return email


	def clean_mobile(self):
		mobile = self.cleaned_data.get("mobile")
		try:
			a = int(mobile)
		except:
			raise forms.ValidationError("Incorrect mobile number")
		if len(mobile)!=10:
			raise forms.ValidationError("Incorrect mobile number")
		elif len(Profile.objects.filter(mobile=mobile)):
			raise forms.ValidationError("Mobile Already Registered")

		return mobile

	def clean_username(self):
		username = self.cleaned_data.get("username")
		if len(User.objects.filter(username=username)):
			raise forms.ValidationError("Username already has been taken")

		return username

	def clean_password(self):
		password = self.cleaned_data.get("password")
		if len(password)<6:
			raise forms.ValidationError("Password must be at least 6 characters")

		return password

	def clean_cpassword(self):
		password = self.cleaned_data.get("password")
		cpassword = self.cleaned_data.get("cpassword")
		if password!=cpassword:
			raise forms.ValidationError("Passwords must match")

		return password


class LoginForm(forms.Form):
	username = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off','autofocus':'on','class':'form-control', 'placeholder':'Username'}))
	password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Password'}))

	def clean_username(self):
		username = self.cleaned_data.get("username")
		if len(User.objects.filter(username=username))==0:
			raise forms.ValidationError("Username does not exist")

		return username

	def clean_password(self):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError("Wrong Username or Password")
		return password
