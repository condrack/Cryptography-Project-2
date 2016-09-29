# Cryptography-Project-2
Python client/server encryption application with mac and hash
Taylor Condrack
Cryptography
Project 2

	This program is written in Python 2.7. Run on two separate instances of
the cse machines. They should be the same machine such as two instances of 
cse02.cse.unt.edu. Execute "python server.py" on one machine and
"python client.py" on the other.
	Upon starting the communication between the server and client, the
server creates the key pair using routines from Crypto.PublicKey RSA. The client
prompts the server and waits for it to send the public key that it has created.
The client encrypts two separate keys using the public key it reveived from the 
server. Then it sends both back. In order to send the key objects I use python 
pickles to serialize the keys and convert them back when received. After the server
reveives both keys it decrypts them with its private key. The first key from the client
is used to encrypt for the triple des system. The second is used to verify the signature
of the senders. 
	The server program uses the Triple Des
encryption algorithm. The MAC method I used in the project was a hash MAC
I used python modules Crypto.Cipher and Crypto.Hash. MD5 is the default 
hashing algorithm used by the python routines used in the program. Given
an input string, the MD5 hash algorithm outputs a hash of lengh 128-bit.
This MAC is sent with the original string. The receiver of these two 
parameters uses its key to calculate the hash with the original string 
it was sent. The program compares its own computed tag with the tag it 
received. If they are equal it shows that the message's integrity has not
been compromised.
	If the MAC computed on the plaintext is verified, the server will encrypt
the plaintext, compute the MAC on the new cipher text, and send both cipher text
and new MAC to the client. The client will then verify the MAC on the cipher text. 
If the verification is not successful, the client's program will print "error". 
I purposedly made this the error message if the second MAC is not verified because
there is no verification done if the first MAC on the plaintext is successful, 
but the second one fails. Having this error message reveals less information to 
potential attackers. 
	If the MAC computed on the plaintext is not verified, the server will compute
the new MAC on the error message and send it back to the client. If the client 
verifies the MAC on the error message, the client's program will display the sent
message "MAC VERIFICATION FAILED". 
	If all MAC's fail verification, the message "error" will be displayed on the client's
display. 

----------------------------------------------------------------------------------------------

Sample Input

plaintext> this text will be encrypted into the cipher text

Sample output if MAC is verified:

working...

Encrypted: \xd4\x97\xd9\x97\xbd\xb2\xc9\xea\'\x93\x8e&eS,\xefq
\x7f$[\xfeT\xe9\x17\xe6( K4\x96\x89\xeeg\x91\xa1\x8f\x1a7 i\xe9
\xe5\x8e\x10\xc1\x8d\xd8\x8f

Sample output if MAC is not verified when plaintext is sent:

MAC VERIFICATION FAILED

Sample output if MAC is not verified for a second time when sending back
the verification error message:

Error
