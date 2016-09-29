#Taylor Condrack
from Crypto.Hash import HMAC
from Crypto.PublicKey import RSA
import socket
import sys
import random
import time
import cPickle

#creates socket and port 
created=socket.socket()
port = 8764
hostname=socket.gethostname()
created.connect((hostname,port))

#client recieves the public key from server as a serialized object
publickey_string=created.recv(1024)

#it converts the pickle into the key
publickey=cPickle.loads(publickey_string)

# 2 keys will be encrypted using the public key
key1='plyugbmj'
key2='lokhyvmo'

#creates initial tag using the second secret key
tag=HMAC.new(key2)
#i create a separate tag to verify incoming packets
verify=HMAC.new(key2)

#encrypt the two keys using the servers public key
enckey1=publickey.encrypt(key1,32)
enckey2=publickey.encrypt(key2,32)
enckey1_string=cPickle.dumps(enckey1)
enckey2_string=cPickle.dumps(enckey2)

#sends the encrypted keys to server
created.send(enckey1_string)
time.sleep(1)
created.send(enckey2_string)

#prompts for plaintext to be encrypted
data=raw_input("plaintext > ")
#computes mac on plaintext

tag.update(data)
#sends packets separtely
#the sleeps is to sync the sends and receives on server side
#created.send(password)
#haptic feedback for user
print("working...")
time.sleep(1)
created.send(data)
time.sleep(1)
tags=tag.hexdigest()
created.send(tags)

#receives feedback either cipher text or error message
feedback=created.recv(1024)

feedback2=created.recv(1024)

#computes mac on feedback to verify mac
verify.update(feedback2)

if verify.hexdigest()==feedback:
	print("Encrypted: "+feedback2)
else:
#vague error incase mac fails for a second time
	sys.exit("error")

#close connection
created.close
