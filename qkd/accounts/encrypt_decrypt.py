import base64
from cryptography.fernet import Fernet
from .models import secret_keys,secret_keys_receiver

def encryption(id,msg):
	print("asdff")
	key = secret_keys.objects.filter(id = id)
	key = key[0].sender_key
	print(type(msg))
	print(type(key))
	# encoded_message = msg.encode()
	# f = Fernet(key)
	# encrypted_message = f.encrypt(encoded_message)

	# print(encrypted_message)
	encrypted_message = base64.b64encode((msg).encode('utf-8'))
	# encrypted_message = b64encode(msg)

	return encrypted_message

def decryption(id,msg):
	print("asdff")
	key = secret_keys_receiver.objects.filter(id = id)
	key = key[0].receiver_key
	print(type(msg))
	print(type(key))
	# encoded_message = msg.encode()
	# f = Fernet(key)
	# encrypted_message = f.encrypt(encoded_message)

	# print(encrypted_message)
	msg = (base64.b64decode(msg)).decode('utf-8')
	# encrypted_message = b64encode(msg)

	return msg