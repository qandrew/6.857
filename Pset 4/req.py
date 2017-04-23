#wut

from flask import abort, Flask, jsonify, request
from os import urandom
from struct import unpack
import speck
import json
import urllib2

NODE_URL = "http://6857speck.csail.mit.edu:4000/?num="
SEARCH = 1

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
	#of the inputs before the two XOR functions to be 0
	return isBit(preShift(x,y),index) == 0 and isBit(speck.ROL(y,3),index) == 0	

def avgVal(arraytoSearch, arrayWithInd):
	if len(arraytoSearch) == 0:
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
	newAr = []
	
	dictOfIndex0 = {}
	for i in xrange(64):
		dictOfIndex0[i] = [] #initiate arrays

	for ind in xrange(len(array)):
		elt = array[ind]
		# print ind, elt
		for i in xrange(64):
			if checkIfBothIndex0(elt[0],elt[1],i):
				dictOfIndex0[i].append(ind)
			# newAr.append(ind)

	print "\nDICTS!!"
	FUCKTHIS = 0
	for key in xrange(63,-1,-1): # iterate from 63 to 0
	# for key in dictOfIndex0:
		av = avgVal(array,dictOfIndex0[key])
		# print key, dictOfIndex0[key], "\n\t", avgVal(array,dictOfIndex0[key])
		print key, len(dictOfIndex0[key]), av
		FUCKTHIS <<= 1
		if av > 2048:
			FUCKTHIS += 1
	print bin(FUCKTHIS)
	# print dictOfIndex0
	# s = 0
	# for elt in newAr:
	# 	s += elt[2]
	# print s
	# print s/len(newAr)




