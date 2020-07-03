from django.shortcuts import render
import time
from numpy import matrix
from math import pow, sqrt
from random import randint
import sys, argparse
from accounts.quantum_channel import *
from .models import secret_keys

def func(request):
	ret = list()
	N = 128
	key = secret_keys(sender_key = "" , receiver_key = "")
	key.save()
	idx = key.id
	key = ""
	for i in range (N):
		print ("############# {0} #############".format(str(i)))
		ret.append(QKD(16,idx,verbose = True ,eve_present = True))
		
		print ("###############################".format(str(i)))
	secret_key = secret_keys.objects.filter(id= idx)
	print("sender key :"+secret_key[0].sender_key)
	print("receiver_key: "+secret_key[0].receiver_key)
	
	t = "{0:.2f}".format(float(ret.count(True))*100.0/float(N))
	u = "{0:.2f}".format(float(ret.count(False))*100.0/float(N))
	print ("True: {0} <{1}%>".format(ret.count(True),str(t)))
	print ("False: {0} <{1}%>".format(ret.count(False),str(u)))

	key = secret_keys.objects.filter(id = idx)
	return render(request,'accounts/index.html', {'key' : key[0]})

