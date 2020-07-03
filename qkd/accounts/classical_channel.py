from accounts.sender import receiver_basis,receiver_bits

def exchange_basis(N,bob_basis):
	alice_basis = receiver_basis(N,bob_basis)
	return alice_basis

def exchange_bits(bob_key,idx):
	alice_key = receiver_bits(bob_key,idx)
	return alice_key
