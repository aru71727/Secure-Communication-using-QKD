from django.shortcuts import render,redirect
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
from accounts.receiver import receiver_msg,receive_msg
from accounts.encrypt_decrypt import *


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
	profiles = Profile.objects.all()
	return render(request,'accounts/index.html',{'profiles': profiles })
	




def chat(request,s_idx,r_idx):
	profiles = Profile.objects.all()
	# print(int(s_idx))
	# print(int(r_idx))
	# print(profiles)

	sender = Profile.objects.get(user=s_idx)
	# print(sender)
	receiver = Profile.objects.get(id=r_idx)
	# print(receiver)
	receiver = receiver.user
	sender  = sender.user
	seen = False
	add = 0
	msg = Messages.objects.filter(sender = sender , receiver = receiver)
	r_msg = Messages.objects.filter(sender = receiver , receiver = sender)

	r_name = receiver
	r_seen = False
	r_ex = 0
	if len(r_msg) != 0:
		r_seen = r_msg[0].seen
		r_msg = r_msg[0]
		r_ex = 1

	if len(msg) == 0:
			add = 1
	else:
		msg = msg[0]
		seen = msg.seen
	# print(seen)
	# print(add)
	# print(msg.sender)
	pro = list()
	for i in profiles:
		if i.user != sender:
			pro.append(i)
			
	params = {'profiles':pro,'msg': msg,'add':add,'seen':seen,'idx':r_idx,'r_name':r_name,'r_msg':r_msg,'r_seen':r_seen,'r_ex':r_ex}
	
	return render(request,'accounts/chat.html',params)






def reviews(request,id,idx,add):
	id=int(id)
	# print(id)
	# print(int(idx))
	if request.method == "POST":
		msg = request.POST.get("message")
	print(msg)


	ret = list()
	N = 72
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
	t = "{0:.2f}".format(float(ret.count(True))*100.0/float(N))
	u = "{0:.2f}".format(float(ret.count(False))*100.0/float(N))
	# print ("True: {0} <{1}%>".format(ret.count(True),str(t)))
	# print ("False: {0} <{1}%>".format(ret.count(False),str(u)))

	print("Exchanged Secret keys")
	key = s_key(s_idx)
	print("Sender's secret key")
	print(key)
	key = r_key(r_idx)
	print("Receiver's secret key")
	print(key)
	sender = Profile.objects.get(user=id)
	# print(sender.user)
	receiver = Profile.objects.get(id=idx)
	# print(receiver.user)
	sender = sender.user
	receiver = receiver.user
	
	add = int(add)
	# print(type(s_idx))

	if add == 1:
		info = Messages(sender = sender, receiver = receiver, s_msg_body = "",r_msg_body="", seen = False,index = s_idx)
		info.save()
		i = info.id
		sender_msg(i,msg)
		
	else:

		info = Messages.objects.filter(sender = sender , receiver = receiver).update( s_msg_body = "",r_msg_body="",seen = False, index = s_idx)
		
		i = info

		sender_msg(i,msg)
	print("Message to send :")
	print(msg)
	msg = encryption(s_idx,msg)
	print("Encrypted Msg : ")
	print(msg)
	
	receive_msg(i,msg)
	info = Messages.objects.filter(sender = sender , receiver = receiver).update(seen = True)
		
	msg = decryption(r_idx,msg)
	print("Decrypted Message :")
	print(msg)

	return redirect('accounts:chat', s_idx= id, r_idx = idx)




def decrypt(request,id,idx,info,r_idx):

	info = Messages.objects.filter(id=info)
	print(info)

	print("hgsahgas")
	msg = decryptin(info)
	print(msg)
	receiver_msg(info,msg)
	for i in info:
		xyz = i.id
		Messages.objects.filter(id=xyz).update(seen = False)
	return redirect('accounts:chat', s_idx= id, r_idx = idx)

