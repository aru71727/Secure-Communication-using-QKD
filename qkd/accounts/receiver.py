from .qubit import qubit
from .quantum import quantum_user
from random import randint
from .models import secret_keys
from accounts.classical_channel import exchange_bits, exchange_basis

receiver_bits = list()
receiver_basis = list()
bob_key = list()

def receiver(N,alice_qubits,idx):
	bob_basis = generate_random_bits(N)
	bob = quantum_user("Bob")
	bob_bits = bob.receive(data = alice_qubits,basis = bob_basis)
	receiver_basis = bob_basis
	receiver_bits = bob_bits
	sender_basis = exchange_basis(N,receiver_basis)
	bob_key.clear()
	for i in range(N):
		if sender_basis[i] == receiver_basis[i]:
			bob_key.append(receiver_bits[i])


	alice_key = exchange_bits(bob_key,idx)
	if alice_key != bob_key:
		key = False
		length = None
		# print ("Encription key mismatch, eve is present.")
	else:
		key = True
		length = len(bob_key)
		#print ("Successfully exchanged key!")
		
		key_length = 128
		key_value = (hex(int(''.join([ str(i) for i in alice_key]), 2))[2:key_length + 2])
		secret_key = secret_keys.objects.filter(id = idx)
		secret_key = secret_key[0].receiver_key+key_value
		secret_keys.objects.filter(id = idx).update(receiver_key = secret_key)
	print ("Bob Key : {} " .format(bob_key))	
	return key


def generate_random_bits(N):
	aux = list()
	for i in range(N):
		aux.append(randint(0,1))
	return aux

