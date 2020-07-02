from .qubit import qubit
from .quantum import quantum_user
from random import randint

def Eve(N,alice_qubits):
	eve_basis = generate_random_bits(N)
	eve = quantum_user("Eve")
	eve_bits = eve.receive(data=alice_qubits,basis=eve_basis)
	alice_qubits = eve.send(data=eve_bits,basis=eve_basis)
	return alice_qubits
	
def generate_random_bits(N):
	aux = list()
	for i in range(N):
		aux.append(randint(0,1))
	return aux


