#Taylor Condrack
import socket
#module for DES3 encryption routines
from Crypto.Cipher import DES3
from Crypto.Hash import HMAC
from Crypto.PublicKey import RSA
from Crypto import Random
import random
import sys
import time
import cPickle

#server creates a key pair of a public and private key
#converts to serialized object to send over socket
random_gen = Random.new().read
key = RSA.generate(1024, random_gen)
publickey=key.publickey()
publickey_string=cPickle.dumps(publickey)

#creates socket and port number
created=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=8764

error=b'MAC VERIFICATION FAILED'

#gets server name and binds it with the port number
hostname=socket.gethostname()
created.bind((hostname,port))
#waits for client to connect
created.listen(2)
#creates the address tuple with the socket, ip, and port
(client,(ip, p))=created.accept()

#prints connection confirmation and address
print 'connection established form ',p
#responds to client with necessary parameters and cipher info

#recieves packet form client
client.send(publickey_string)
enckey1_string=client.recv(1024)
time.sleep(1)
enckey2_string=client.recv(1024)
enckey1=cPickle.loads(enckey1_string)
enckey2=cPickle.loads(enckey2_string)

#decrypts the secret keys received from client
deckey1=key.decrypt(enckey1)
deckey2=key.decrypt(enckey2)

#computes initial tag using key 2
tag=HMAC.new(deckey2)
#i create a second tag to verify incoming packets
verify=HMAC.new(deckey2)

#error checking: the key made from the pasword needs to be 8 bytes
#this concatenates bytes to the key if it is too short
#it truncates bytes if the key is too long
if len(deckey1) < 16:
	add=16-len(deckey1)
	for i in range(add):
		deckey1=deckey1+' '
elif len(deckey1) >16:
	deckey1=deckey1[:16]

#recieves plaintext packet from the client
data=client.recv(1024)

tagr=client.recv(1024)
#computes mac on received plaintext
tag.update(data)

tagr="failed"
#verifys mac sent with plaintext with servers verify tag and plaintext
if tag.hexdigest()!=tagr:
	verify.update(error)
	client.send(verify.hexdigest())
	time.sleep(1)
	client.send(error)
	sys.exit()


#this forces the plaintext to contain bytes that are a multiple of 8
if len(data)%8!=0:
	add=8-len(data)%8
	for i in range(add):
		data=data+' '


#creates initilized vector with the correct block size
iv=Random.new().read(DES3.block_size)
#creates des variable from key in CFB mode and the iv
des=DES3.new(deckey1,DES3.MODE_CFB,iv)
#encrypts the plaintext using DES3 algorithm
ciphertext=des.encrypt(data)
#returns the cipher text to the client
ciphertext=ciphertext.encode('string_escape')

#computes mac on cipher text
verify.update(ciphertext)

client.send(verify.hexdigest())
time.sleep(1)
client.send(ciphertext)

#close connection
client.close()

