#gbox
global gbox
gbox = '5f f3 a7 7b ae 8f 8a fc ea 43 dd 35 33 0c 73 0e f7 c4 e6 0b 97 50 4a 27 f5 18 6e 0a d4 45 cb 42 c2 7f c5 ce 99 3c 30 e4 f9 38 ac 1f 6f 09 08 01 11 a4 58 96 b4 67 cd 84 20 2e 9f 5b af 90 de 76 d7 fa 9c 06 17 6d ed 63 82 69 cc 93 79 ec 21 29 71 8d 28 d8 53 98 52 2f 89 2c d2 a1 5c 44 49 13 c0 86 3d 88 ba a5 d9 59 26 32 70 9a 80 a0 95 b0 4b 2b 04 85 83 da 15 23 0d a9 75 19 f0 be 54 c9 b9 31 14 f1 4f d6 bf 6a 7e 25 41 4e 5a 7d ab 55 2a 51 78 8e 57 fb 4d 60 8c 68 9e 24 22 e8 e3 07 6b bb 1b a8 e7 9b c3 36 3f 34 b5 fd 0f 74 e2 c1 5d e5 39 f4 48 8b 92 7c dc 1a 65 81 91 3a df ad d0 72 a2 7a ff 66 1e d5 eb 64 c7 ef 4c 05 cf e0 2d f8 d3 bc 56 b6 10 b8 03 b3 77 b7 c8 3b b2 d1 b1 a6 6c 61 94 46 87 ee e9 db 5e 37 02 1d bd 00 1c f6 ca 12 c6 62 47 3e e1 40 aa a3 f2 fe 9d 16'
gbox = gbox.split(" ")

# get all ciphertext
ciphs = []
with open('tenciphs.txt') as inputfile:
    for line in inputfile:
        temp = line.strip().split(' ')
        ciphs.append(temp)

def xor(s1,s2, base=16):
	#xors two strings that are in base format
	t1 = int(s1,base)
	t2 = int(s2,base)
	t3 = t1 ^ t2 #xor
	if base == 16:
		return format(t3, 'x') 
	elif base == 10:
		return t3

def g(s1): #apply one time pad function g
	i = int(s1,16)
	t3 = int(gbox[i],16) ^ i
	return format(t3, 'x') 

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

def decrypt(cipher,pad):
	pass

#test stuff
mes = ['a1', 'a1', '44']
pad = ['ff', '00', '00']
# print mes
out = encrypt(mes,pad)
# print out
# print encrypt(out,pad)

# we know that the pad must map all messages M1 - M10 to C1 - C10
# where M1 - M10 are printable characters (decimal value 32-126)

# for i in xrange(len(ciphs)):
# 	for j in xrange(i+1,len(ciphs)):
# 		temp = xor(ciphs[i][0],ciphs[j][0])
# 		print i,j, ciphs[i][0], ciphs[j][0], temp

for i in xrange(3): # xrange(len(ciphs[0])):
	temp = xor(ciphs[0][i],ciphs[1][i])
	print ciphs[0][i],ciphs[1][i], temp, format(int(temp,16),'#010b')

