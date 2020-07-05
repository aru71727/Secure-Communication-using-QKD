import base64
from cryptography.fernet import Fernet
from .models import secret_keys,secret_keys_receiver,Messages

def encryption(id,msg):
	key = secret_keys.objects.filter(id = id)
	key = key[0].sender_key

	# encoded_message = msg.encode()
	# f = Fernet(key)
	# encrypted_message = f.encrypt(encoded_message)

	# print(encrypted_message)
	encrypted_message = base64.b64encode((msg).encode('utf-8'))
	# encrypted_message = b64encode(msg)

	return encrypted_message

def decryption(id,msg):
	key = secret_keys_receiver.objects.filter(id = id)
	key = key[0].receiver_key
	# encoded_message = msg.encode()
	# f = Fernet(key)
	# encrypted_message = f.encrypt(encoded_message)

	# print(encrypted_message)
	msg = (base64.b64decode(msg)).decode('utf-8')
	# encrypted_message = b64encode(msg)

	return msg

def s_key(s_idx):
	secret_key = secret_keys.objects.filter(id= s_idx)
	secret_key= secret_key[0].sender_key
	return secret_key

def r_key(r_idx):
	secret_key = secret_keys_receiver.objects.filter(id= r_idx)
	secret_key= secret_key[0].receiver_key
	return secret_key

def decryptin(id):
	print("asdsssfssssssss")
	print(id)
	for i in id:

		# secret_key = Messages.objects.filter(id= i)
		# secret_key = secret_key[0].s_msg_body
		secret_key = i.s_msg_body
	print(secret_key)
	print("abc")
	return secret_key


