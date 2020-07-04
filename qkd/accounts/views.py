from django.shortcuts import render
import time
from numpy import matrix
from math import pow, sqrt
from random import randint
import sys, argparse
from django.urls import reverse
from accounts.quantum_channel import *
from .models import secret_keys,secret_keys_receiver,Messages
from .models import Profile
from .forms import RegistrationForm,LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from accounts.sender import sender_msg
from accounts.receiver import receiver_msg
from accounts.encrypt_decrypt import encryption,decryption
# from accounts.decryption import decryption


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
	# ret = list()
	# N = 128
	# key = secret_keys(sender_key = "" )
	# key.save()
	# s_idx = key.id
	# key =  secret_keys_receiver(receiver_key = "" )
	# key.save()
	# r_idx = key.id
	
	# key = ""
	# for i in range (N):
	# 	print ("############# {0} #############".format(str(i)))
	# 	ret.append(QKD(16,s_idx,r_idx,verbose = True ,eve_present = True))
		
	# 	print ("###############################".format(str(i)))
	# secret_key = secret_keys.objects.filter(id= s_idx)
	# print("secret_key"+secret_key)
	# secret_keys_receiver = secret_keys_receiver.objects.filter(id= s_idx)
	# print("secret_keys_receiver"  + secret_keys_receiver)
	# print("sender key :"+secret_key[0].sender_key)
	# print("receiver_key: "+secret_key[0].receiver_key)
	
	# t = "{0:.2f}".format(float(ret.count(True))*100.0/float(N))
	# u = "{0:.2f}".format(float(ret.count(False))*100.0/float(N))
	# print ("True: {0} <{1}%>".format(ret.count(True),str(t)))
	# print ("False: {0} <{1}%>".format(ret.count(False),str(u)))
	
	profiles = Profile.objects.all()
	return render(request,'accounts/index.html',{'profiles': profiles })
	




def chat(request,s_idx,r_idx):
	profiles = Profile.objects.all()
	print(int(s_idx))
	print(int(r_idx))
	print(profiles)

	sender = Profile.objects.get(user=s_idx)
	print(sender)
	receiver = Profile.objects.get(id=r_idx)
	print(receiver)
	receiver = receiver.user
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
	params = {'profiles':profiles,'msg': msg,'add':add,'seen':seen,'idx':r_idx}
	
	return render(request,'accounts/chat.html',params)



def reviews(request,id,idx,add):
	id=int(id)
	print(id)
	print(int(idx))
	if request.method == "POST":
		msg = request.POST.get("message")
	print(msg)


	ret = list()
	N = 128
	key = secret_keys_receiver(receiver_key = "" )
	key.save()
	r_idx = key.id
	key = secret_keys(sender_key = "" ,r_index=key)
	key.save()
	s_idx = key.id
	

	
	for i in range (N):
		print ("############# {0} #############".format(str(i)))
		ret.append(QKD(16,s_idx,r_idx,verbose = True ,eve_present = True))
		
		print ("###############################".format(str(i)))
	# secret_key = secret_keys.objects.filter(id= s_idx)
	# print(secret_key)
	# print("sender key :"+secret_key[0].sender_key)
	# print("receiver_key: "+secret_key[0].receiver_key)
	
	t = "{0:.2f}".format(float(ret.count(True))*100.0/float(N))
	u = "{0:.2f}".format(float(ret.count(False))*100.0/float(N))
	print ("True: {0} <{1}%>".format(ret.count(True),str(t)))
	print ("False: {0} <{1}%>".format(ret.count(False),str(u)))

	# key = secret_keys_receiver.objects.filter(id = r_idx)
	# print(key)

	
	sender = Profile.objects.get(user=id)
	print(sender)
	receiver = Profile.objects.get(id=idx)
	print(receiver)
	receiver = receiver.user
	
	add = int(add)
	print(type(s_idx))
	if add == 1:
		info = Messages(sender = sender, receiver = receiver, s_msg_body = "",r_msg_body="", seen = False,index = s_idx)
		info.save()
		info = info.id
		sender_msg(info,msg)
		
	else:

		info = Messages.objects.get(sender = sender , receiver = receiver)
		print("nvnhk")
		info = info.id
		sender_msg(info,msg)
	msg = encryption(s_idx,msg)
	print(msg)
	receiver_msg(info,msg)
	msg = decryption(r_idx,msg)
	print(msg)
	receiver_msg(info,msg)
	return render(request,'accounts/in.html')