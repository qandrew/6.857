"""
Speck128/128
https://en.wikipedia.org/wiki/Speck_(cipher)
"""

uint64 = lambda x: x & ((1 << 64) - 1)
ROL = lambda x, r: uint64(x << r) | (x >> (64 - r))
ROR = lambda x, r: (x >> r) | uint64(x << (64 - r))

def R(x, y, k):
    x = ROR(x, 8)
    x = uint64(x + y)
    x = x ^ k
    y = ROL(y, 3)
    y = y ^ x
    return x, y

table = [bin(i).count('1') for i in range(256)]
def ones(n):
    w = 0
    while n:
        w += table[n & 255]
        n >>= 8
    return w

def leak(a, b, x, y, r):
    x, y = R(x, y, b)
    s = ones(x) + ones(y)
    for i in range(r - 1):
        a, b = R(a, b, i)
        x, y = R(x, y, b)
        s += ones(x) + ones(y)
    return s