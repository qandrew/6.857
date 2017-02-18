#gbox
global gbox
gbox = '5f f3 a7 7b ae 8f 8a fc ea 43 dd 35 33 0c 73 0e f7 c4 e6 0b 97 50 4a 27 f5 18 6e 0a d4 45 cb 42 c2 7f c5 ce 99 3c 30 e4 f9 38 ac 1f 6f 09 08 01 11 a4 58 96 b4 67 cd 84 20 2e 9f 5b af 90 de 76 d7 fa 9c 06 17 6d ed 63 82 69 cc 93 79 ec 21 29 71 8d 28 d8 53 98 52 2f 89 2c d2 a1 5c 44 49 13 c0 86 3d 88 ba a5 d9 59 26 32 70 9a 80 a0 95 b0 4b 2b 04 85 83 da 15 23 0d a9 75 19 f0 be 54 c9 b9 31 14 f1 4f d6 bf 6a 7e 25 41 4e 5a 7d ab 55 2a 51 78 8e 57 fb 4d 60 8c 68 9e 24 22 e8 e3 07 6b bb 1b a8 e7 9b c3 36 3f 34 b5 fd 0f 74 e2 c1 5d e5 39 f4 48 8b 92 7c dc 1a 65 81 91 3a df ad d0 72 a2 7a ff 66 1e d5 eb 64 c7 ef 4c 05 cf e0 2d f8 d3 bc 56 b6 10 b8 03 b3 77 b7 c8 3b b2 d1 b1 a6 6c 61 94 46 87 ee e9 db 5e 37 02 1d bd 00 1c f6 ca 12 c6 62 47 3e e1 40 aa a3 f2 fe 9d 16'
gbox = gbox.split(" ")
# print len(gbox)

def xor(s1,s2):
	t1 = int(s1,16)
	t2 = int(s2,16)
	t3 = t1 ^ t2 #xor
	return format(t3, 'x') 

def g(s1):
	i = int(s1,16)
	t3 = int(gbox[i],16) ^ i
	return format(t3, 'x') 

print xor(g('a1'),g('a2'))
print g(xor('a1','a2'))

def encrypt(message, pad):
	out = []
	assert len(message) <= len(pad)
	for i in xrange(len(message)):
		if i == 0:
			temp = xor(message[i],g(pad[i]))
			out.append(temp)
		else:
			temp = g(xor(pad[i],out[i-1]))
			out.append(xor(message[i],temp))
	return out

mes = ['a1', 'a1', '44']
pad = ['ff', '00', '00']
print mes
out = encrypt(mes,pad)
print out
print encrypt(out,pad)

ciphs = []
with open('tenciphs.txt') as inputfile:
    for line in inputfile:
        temp = line.strip().split(' ')
        ciphs.append(temp)

print len(ciphs)


