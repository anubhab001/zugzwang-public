#!/usr/bin/env python3

## Reference implementation of the proof-of-concept cipher, 'ZUGZWANG' (concrete instance)
## Requires PyCryptodome <https://pycryptodome.readthedocs.io/>, tested with version 3.14.1


key = 0x3cf28000471a74d22d81b6c98a3dbe33 # Secret master key
backdoor = 0x1831bcaa5bee08e639864e4823183090 # Secret backdoor entry
plaintext = 0x9eac455e039a58928e163658e1493a20 # Public plaintext

#plaintext = backdoor ### When uncommented, this recovers the key


n = 4 # Number of Feistel rounds
size = 128 # State size
branch = 2 # Number of Feistel branches


from Crypto.Cipher import AES
from Crypto.Hash import SHAKE128


def get_bytes(x):
    return int.to_bytes(x, byteorder="little", signed=False, length=size//8)

def get_int(y):
    return int.from_bytes(y, byteorder="little", signed=False)

def pad_zero(z, l_nibble):
    return (hex(z)[2:]).zfill(l_nibble)

def gen_fe_round_key(k, n):
    K = []
    for i in range(0, n):
        K.append(get_int(get_enc(Ky=key, msg=get_bytes(i))))
    
    return K

def truncate(data):
    data_hex = pad_zero(data, l_nibble=size//4) 
    return int('0x'+data_hex[0:size//(branch*4)], 16), int('0x'+data_hex[size//(branch*4):], 16)

def get_hash(msg): 
    H = SHAKE128.new()
    H.update(data=get_bytes(msg))
    return get_int(H.read(size//8)) # Hash output is fixed at `size` bits

def get_enc(msg, Ky):
    E = AES.new(Ky, AES.MODE_ECB)
    return E.encrypt(msg)


# Convert to bytes
plaintext = get_bytes(plaintext) 
key = get_bytes(key) 
backdoor = get_bytes(backdoor) 


# Get Feistel round keys
F_round_keys = gen_fe_round_key(k=key, n=n)

# Get post-whitening keys
KL, KR = truncate(data=get_int(key))
p0, p1 = truncate(data=get_int(backdoor))

Hp = get_hash(msg=p0), get_hash(msg=p1)

C0, C1 = truncate(data=get_int(plaintext))

# Feistel round operation
for i in range(n):
    j = i % 2

    alpha = truncate(get_int(get_enc(Ky=get_bytes(F_round_keys[i]), msg=get_bytes(Hp[j]))))[0]
    
    beta = truncate(get_int(get_enc(Ky=get_bytes(F_round_keys[i]), msg=get_bytes(get_hash(C0)))))[0]

    f = alpha ^ beta # Feistel round function

    C1 = f ^ C1 # Update right branch

    if i < n-1: # Do not swap branches in last round
        C0, C1 = C1, C0 # Swap branches
    
# Post-whiten
C0, C1 = C0 ^ KL, C1 ^ KR


# Display output
plaintext = pad_zero(get_int(plaintext), l_nibble=size//4) # Hexadecimal string
key = pad_zero(get_int(key), l_nibble=size//4) # Hexadecimal string
backdoor = pad_zero(get_int(backdoor), l_nibble=size//4) # Hexadecimal string
ciphertext = pad_zero(C0, l_nibble=size//(branch*4)) + pad_zero(C1, l_nibble=size//(branch*4)) # Hexadecimal string

print ('Key:\t\t', key)
print ('Backdoor Entry:\t', backdoor)
print ('Plaintext:\t', plaintext)
print ('Ciphertext:\t', ciphertext)

if backdoor == plaintext:
    if n % 2 == 0: # Even round
        l, r = p1, p0
    else: # Odd round
        l, r = p0, p1
    
    K_recovered = pad_zero(z = C0 ^ l, l_nibble=size//(branch*4)) + pad_zero(z = C1 ^ r, l_nibble=size//(branch*4)) # Hexadecimal string
    
    if  K_recovered == key:
        print('\033[31mRecovered Key:\t', (K_recovered), end='\033[0m\n')
    else:
        assert False