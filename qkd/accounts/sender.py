from .qubit import qubit
from .quantum import quantum_user
from random import randint
from .models import secret_keys,Messages
# # from accounts.channel import encrypt_decrypt
# from accounts.channel import encrypt_decrypt

sender_basis = list()
sender_bits = list()
alice_key = list()
alice_basis = list()


def sender(N):
	alice_basis = generate_random_bits(N)
	alice_bits = generate_random_bits(N)
	alice = quantum_user("Alice")
	alice_qubits = alice.send(data=alice_bits,basis=alice_basis)
	sender_basis.clear()
	sender_bits.clear()
	for i in range(N):
		sender_basis.append(alice_basis[i])
		sender_bits.append(alice_bits[i])
	return alice_qubits

def receiver_basis(N,receiver_basis):
	alice_key.clear()
	for i in range(N):
		if sender_basis[i] == receiver_basis[i]:
			alice_key.append(sender_bits[i])
	return sender_basis


def receiver_bits(bob_key,s_idx):
	if alice_key != bob_key:
		key = False
		length = None
		print ("Encription key mismatch, eve is present.")
	else:
		key = True
		length = len(alice_key)
		print ("Successfully exchanged key!")
		print ("Key Length: " + str(length))
		
		key_length = 128
		key_value = (hex(int(''.join([ str(i) for i in alice_key]), 2))[2:key_length + 2])
		secret_key = secret_keys.objects.filter(id= s_idx)
		secret_key = secret_key[0].sender_key+key_value
		secret_keys.objects.filter(id= s_idx).update(sender_key = secret_key)
	print  ("Alice Key : {} " .format(alice_key))
	return alice_key



def generate_random_bits(N):
	aux = list()
	for i in range(N):
		aux.append(randint(0,1))
	return aux

# def encryption(info,msg):
# 	info.update(s_msg_body = msg)
# 	encrypt_decrypt(info,msg)
# 	return

def sender_msg(info,msg):
	Messages.objects.filter(id=info).update(s_msg_body = msg)
	# encrypt_decrypt(info,msg)
	return


