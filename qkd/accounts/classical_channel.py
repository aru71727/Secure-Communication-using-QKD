from accounts.sender import receiver_basis,receiver_bits

def exchange_basis(N,bob_basis):
	alice_basis = receiver_basis(N,bob_basis)
	return alice_basis

def exchange_bits(bob_key):
	alice_key = receiver_bits(bob_key)
	return alice_key
