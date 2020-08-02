import random
from math import pow

class ElGamal(object):
        
    def __init__(self):
        self.q = random.randint(pow(10, 20), pow(10, 50)) 
        self.g = random.randint(2, self.q) 
    
        self.key = self.gen_key(self.q) # Private key for receiver 
        self.h = self.power(self.g, self.key, self.q) 

        self.k = self.gen_key(self.q) # Private key for sender
        self.s = self.power(self.h, self.k, self.q)
        self.p = self.power(self.g, self.k, self.q)

    def gcd(self, a, b):
        if a < b:
            return self.gcd(b, a)
        elif a % b == 0:
            return b
        else:
            return self.gcd(b, a % b)

    # Generating large random numbers
    def gen_key(self, q):
        key = random.randint(pow(10, 20), q)
        while self.gcd(q, key) != 1:
            key = random.randint(pow(10, 20), q)

        return key

    # Modular exponentiation
    def power(self, a, b, c):
        x = 1
        y = a
        while b > 0:
            if b % 2 == 0:
                x = (x * y) % c
            y = (y * y) % c
            b = int(b / 2)

        return x % c

    # Asymmetric encryption
    def encrypt(self, msg):
        en_msg = ''

        for i in range(0, len(msg)):
            en_msg += str(hex(self.s * ord(msg[i]))[2:])

        return en_msg

    # Asymmetric decryption
    def decrypt(self, en_msg, p):
        dr_msg = []
        h = self.power(p, self.key, self.q)
        for i in range(0, len(en_msg)):
            dr_msg.append(chr(int(en_msg[i]/h)))
        return dr_msg