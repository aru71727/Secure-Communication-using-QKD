from django.shortcuts import render
import time
from numpy import matrix
from math import pow, sqrt
from random import randint
import sys, argparse
from django.urls import reverse
from accounts.quantum_channel import *
from .models import secret_keys
from .models import Profile,Messages
from .forms import RegistrationForm,LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse


from django.contrib.auth import (

	authenticate,
	login,
	logout

	)

def loginview(request):
	form = LoginForm(request.POST or None)
	if request.method =="POST":
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			print(username,password)
			user = authenticate(username=username, password=password)
			login(request, user)
			return HttpResponseRedirect(reverse("home"))

	context = {
		'form':form 
	}
	return render(request, 'accounts/login.html', context)


@login_required
def logoutview(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))


	

def registerview(request):
	form = RegistrationForm(request.POST or None)
	
	if request.method=="POST":
	
		if form.is_valid():
			first_name = form.cleaned_data.get('first_name')
			last_name= form.cleaned_data.get('last_name')
			address = form.cleaned_data.get("address")
			mobile = form.cleaned_data.get("mobile")
			gender = form.cleaned_data.get("gender")
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get("username")
			password  = form.cleaned_data.get('password ')
			cpassword  = form.cleaned_data.get('cpassword ')
			
			user, create = User.objects.get_or_create(
			
				first_name=first_name,
				last_name=last_name,
				username=username,
				email=email,

			)
			user.set_password(form.cleaned_data['password'])
			user.save()
			

			pro = Profile(mobile=mobile, address = address , gender=gender, user=user )
			pro.save()

			messages.success(request, "Successfully Saved")
			context={
				"msg":"Successfully Registered!!"
			} 
			
			return render(request,'accounts/messagesdisplay.html',context)
	context = {
		'form':form,
	}
	return render(request, 'accounts/registration.html', context)





def func(request):
	ret = list()
	N = 128
	idx = 1
	# key = secret_keys(sender_key = "" , receiver_key = "")
	# key.save()
	# idx = key.id
	# key = ""
	# for i in range (N):
	# 	print ("############# {0} #############".format(str(i)))
	# 	ret.append(QKD(16,idx,verbose = True ,eve_present = True))
		
	# 	print ("###############################".format(str(i)))
	# # secret_key = secret_keys.objects.filter(id= idx)
	# print("sender key :"+secret_key[0].sender_key)
	# print("receiver_key: "+secret_key[0].receiver_key)
	
	t = "{0:.2f}".format(float(ret.count(True))*100.0/float(N))
	u = "{0:.2f}".format(float(ret.count(False))*100.0/float(N))
	print ("True: {0} <{1}%>".format(ret.count(True),str(t)))
	print ("False: {0} <{1}%>".format(ret.count(False),str(u)))

	# key = secret_keys.objects.filter(id = idx)
	profiles = Profile.objects.all()
	return render(request,'accounts/index.html',{'profiles': profiles })





def chat(request,id,idx):
	profiles = Profile.objects.all()
	# id=int(id)
	# print(id)
	# print(int(idx))
	sender = Profile.objects.filter(user_id=id)
	sender = sender[0].user
	receiver = Profile.objects.filter(user_id=idx)
	receiver = receiver[0].user
	seen = False
	add = 0
	msg = Messages.objects.filter(sender = sender , receiver = receiver)
	

	if len(msg) == 0:
			add = 1
	else:
		msg = msg[0]
		seen = msg.seen
	# print(seen)
	# print(add)
	# print(msg.sender)
	params = {'profiles':profiles,'msg': msg,'add':add,'seen':seen,'idx':idx}
	return render(request,'accounts/chat.html',params)



def reviews(request,id,idx,add):
	id=int(id)
	print(id)
	print(int(idx))
	if request.method == "POST":
		msg = request.POST.get("message")
	print(msg)
	return 