from .qubit import qubit
from .quantum import quantum_user
from random import randint


sender_basis = list()
sender_bits = list()
alice_key = list()
alice_basis = list()
sender_secret_key = ""

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


def receiver_bits(bob_key):
	if alice_key != bob_key:
		key = False
		length = None
	else:
		key = True
		length = len(alice_key)
		print ("Key Length: " + str(length))
		print  ("Alice Key : {} " .format(alice_key))
		key_length = 128
		key_value = (hex(int(''.join([ str(i) for i in alice_key]), 2))[2:key_length + 2])
		sender_secret_key = key_value
	return alice_key


def generate_random_bits(N):
	aux = list()
	for i in range(N):
		aux.append(randint(0,1))
	return aux

