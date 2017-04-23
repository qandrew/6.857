"""
Speck128/128
https://en.wikipedia.org/wiki/Speck_(cipher)
"""
from os import urandom
from struct import unpack

uint64 = lambda x: x & ((1 << 64) - 1)
ROL = lambda x, r: uint64(x << r) | (x >> (64 - r))
ROR = lambda x, r: (x >> r) | uint64(x << (64 - r))

def R(x, y, k):
    x = ROR(x, 8)
    print "x ROR 8 \t", ones(x), "\t", format(x,'064b')
    x = uint64(x + y)
    print "x + y   \t", ones(x), "\t", format(x,'064b')
    x = x ^ k
    print "x XOR k \t", ones(x), "\t", format(x,'064b')
    y = ROL(y, 3)
    print "y ROL 3 \t", ones(y), "\t", format(y,'064b')
    y = y ^ x
    print "y XOR x \t", ones(y), "\t", format(y,'064b')
    return x, y

table = [bin(i).count('1') for i in range(256)]
def ones(n):
    w = 0
    while n:
        w += table[n & 255]
        n >>= 8
    return w

def leak(a, b, x, y, r): 
    # r rounds
    # a, b is the high/low key
    # x, y is the high/low plaintext
    print "x \t", ones(x), "\t", x
    print "y \t", ones(y), "\t", y
    x, y = R(x, y, b) 
    print "x \t", ones(x), "\t", x
    print "y \t", ones(y), "\t", y
    s = ones(x) + ones(y)
    print "round 0", ones(x), "+", ones(y), "=", s
    for i in range(1,r ):
    # for i in range(r - 1):
        print "entering round key k=", i
        a, b = R(a, b, i)
        print "entering round pt"
        x, y = R(x, y, b)
        s += ones(x) + ones(y)
        print "round", i+1, ones(x), "+", ones(y), "=", s
    return s

def r64():
    return unpack("<Q", urandom(8))[0]

if __name__ == "__main__":
    a = 1 #r64()  # high 64 bits of secret key
    b = 2 #r64()  # low 64 bits of secret key
    x = 3 #r64()      # high 64 bits of plaintext
    y = 4 #r64()      # low 64 bits of plaintext
    print 'HIGH a={0:064b}'.format(a), ones(a)
    print 'LOW  b={0:064b}'.format(b), ones(b)
    o = leak(a, b, x, y, r=2) # num of ones in the XOR outputs
    print "o \t", o

    # print ROR(3,1), bin(ROR(3,1))