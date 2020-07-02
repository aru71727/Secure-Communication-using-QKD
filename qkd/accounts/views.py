from django.shortcuts import render
import time
from numpy import matrix
from math import pow, sqrt
from random import randint
import sys, argparse
from accounts.quantum_channel import *

def func(request):
	ret = list()
	N = 128
	for i in range (N):
		print ("############# {0} #############".format(str(i)))
		ret.append(QKD(10,True ,True))
		print ("###############################".format(str(i)))

	t = "{0:.2f}".format(float(ret.count(True))*100.0/float(N))
	u = "{0:.2f}".format(float(ret.count(False))*100.0/float(N))
	print ("True: {0} <{1}%>".format(ret.count(True),str(t)))
	print ("False: {0} <{1}%>".format(ret.count(False),str(u)))
	return render(request,'accounts/index.html')

