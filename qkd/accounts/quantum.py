from .qubit import qubit
class quantum_user():
	def __init__(self,name):
		self.name = name
	def send(self,data,basis):
		"""
		Uso base computacional |0> y |1> para los estados horizontal y vertical.
		Uso base Hadamard |0> + |1> y |0> - |1> para los estados diagonales.
		0 0 -> |0>
		0 1 -> |1>
		1 0 -> |0> + |1>
		1 1 -> |0> - |1>
		"""
		assert len(data) == len(basis), "Basis and data must be the same length!"
		qubits = list()
		for i in range(len(data)):
			if not basis[i]:
				#Base computacional
				if not data[i]:
					qubits.append(qubit(0))
				else:
					qubits.append(qubit(1))
			else:
				#Base Hadamard
				if not data[i]:
					aux = qubit(0)
				else:
					aux = qubit(1)
				aux.hadamard()
				qubits.append(aux)
		return qubits
	def receive(self,data,basis):
		assert len(data) == len(basis), "Basis and data must be the same length!"
		bits = list()
		for i in range(len(data)):
			if not basis[i]:
				bits.append(data[i].measure())
			else:
				data[i].hadamard()
				bits.append(data[i].measure())
		return bits