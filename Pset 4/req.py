#wut

from flask import abort, Flask, jsonify, request
from os import urandom
from struct import unpack
import speck
import json
import urllib2

NODE_URL = "http://6857speck.csail.mit.edu:4000/?num="
# NODE_URL = "http://127.0.0.1:4000/?num="
SEARCH = 1

LOWKEY = 0
# after we found answer
# LOWKEY = 0b1000111001000101101110011101001100000101001110000000011111111101

HIGHKEY = 0
# after we found answer
# HIGHKEY = 0b10000001010100010111011101111101101101101010111110110000111010

def load(count = 1):
	if count<=10000:
		return json.loads(urllib2.urlopen(NODE_URL + str(count)).read())
	else:
		arr = json.loads(urllib2.urlopen(NODE_URL + str(10000)).read())
		count -= 10000
		while count > 10000:
			arr += json.loads(urllib2.urlopen(NODE_URL + str(10000)).read())
			count -= 10000
		arr += json.loads(urllib2.urlopen(NODE_URL + str(count)).read())
		return arr

def isBit(plaintext, index):
	return plaintext & (1 << index)

def preShift(x,y):
	x = speck.ROR(x, 8)
	x = speck.uint64(x + y)
	return x

def checkIfBothIndex0(x,y, index):
	#we are filtering the array such that we want the index bit
	#of the inputs before the two XOR functions in ROUND 0 to be 0
	tx = preShift(x,y)
	ty = speck.ROL(y,3)
	# print 'index', index
	# print 'tx={0:064b}'.format(tx)
	# print 'ty={0:064b}'.format(ty)
	return isBit(preShift(x,y),index) == 0 and isBit(speck.ROL(y,3),index) == 0	

def checkIfBothIndex1(x,y,index):
	#we are filtering the array such that we want the index bit
	#of the inputs before the two XOR functions in ROUND 1 to be 0
	if LOWKEY == 0:
		print "WARNING: low key not set"
		return
	x,y = speck.R(x, y, LOWKEY) #run one round
	return checkIfBothIndex0(x,y, index)

def getHighKeyFromBB(bb,LOWKEY):
	# given "BB" as defined in piazza post, and that we know K2 lowkey
	# return HIGHKEY (k1)
	tempBB = bb ^ speck.ROL(LOWKEY,3)
	tempBB = speck.uint64(tempBB -LOWKEY)
	return speck.ROL(tempBB,8)

def avgVal(arraytoSearch, arrayWithInd):
	if len(arrayWithInd) == 0:
		return 0
	s = 0
	for i in arrayWithInd:
		s += arraytoSearch[i][2]
	return float(s)/float(len(arrayWithInd))

if __name__ == "__main__":
	array = load(100000)
	print "imported"
	# print array
	# a,b,c = array[0]
	# print a, b, c
	
	if LOWKEY == 0:
		# if we haven't found the lowkey yet
		dictOfIndex0 = {}
		for i in xrange(64):
			dictOfIndex0[i] = [] #initiate arrays

		for ind in xrange(len(array)):
			elt = array[ind]
			tx = preShift(elt[0],elt[1])
			ty = speck.ROL(elt[1],3)
			# print 'array index', ind, elt[2]
			# print 'x= {0:064b}'.format(elt[0])
			# print 'Rx={0:064b}'.format(speck.ROR(elt[0], 8))
			# print 'y= {0:064b}'.format(elt[1])
			# print 'tx={0:064b}'.format(tx)
			# print 'ty={0:064b}'.format(ty)
			for i in xrange(64):
				# if checkIfBothIndex0(elt[0],elt[1],i):
				if isBit(tx,i) == 0 and isBit(ty,i) == 0:
					dictOfIndex0[i].append(ind)

		print "\nDICTS L!!"
		FUCKTHIS = 0
		for key in xrange(63,-1,-1): # iterate from 63 to 0
		# for key in dictOfIndex0:
			av = avgVal(array,dictOfIndex0[key])
			# print key, len(dictOfIndex0[key]), dictOfIndex0[key], av
			print key, len(dictOfIndex0[key]), av
			FUCKTHIS <<= 1
			if av > 2048:
				FUCKTHIS += 1
		print bin(FUCKTHIS)

		LOWKEY = FUCKTHIS
	if HIGHKEY == 0:
		# if we've found the lowkey in a previous running of the code
		# now, let's find the highkey

		dictOfIndex1 = {}
		for i in xrange(64):
			dictOfIndex1[i] = [] #initiate arrays

		for ind in xrange(len(array)):
			elt = array[ind]
			# print ind, elt
			for i in xrange(64):
				if checkIfBothIndex1(elt[0],elt[1],i):
					dictOfIndex1[i].append(ind)
		print "\nDICTS H!!"
		FUCKTHIS = 0
		for key in xrange(63,-1,-1): # iterate from 63 to 0
		# for key in dictOfIndex0:
			av = avgVal(array,dictOfIndex1[key])
			# print key, dictOfIndex0[key], "\n\t", avgVal(array,dictOfIndex0[key])
			print key, len(dictOfIndex1[key]), av
			FUCKTHIS <<= 1
			if av > 2048:
				FUCKTHIS += 1
		HIGHKEY = getHighKeyFromBB(FUCKTHIS,LOWKEY)			
		print "\nHIGHKEY!! \t", bin(HIGHKEY)
		print "LOWKEY!! \t", bin(LOWKEY)

	#now test back
	print "checking"
	countCorrect = 0
	for elt in array:
		o = speck.leak(HIGHKEY, LOWKEY, elt[0], elt[1], r=32) # num of ones in the XOR outputs
		# print "our out", o
		if elt[2] == o:
			countCorrect += 1

	print "num correct:", countCorrect, "of", len(array)









