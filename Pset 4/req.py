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
	return json.loads(urllib2.urlopen(NODE_URL + str(count)).read())

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

if __name__ == "__main__":
	array = load(10)
	# print array
	# a,b,c = array[0]
	# print a, b, c
	newAr = []
	
	dictOfIndex0 = {}
	for i in xrange(64):
		dictOfIndex0[i] = [] #initiate arrays

	for ind in xrange(len(array)):
		elt = array[ind]
		print ind, elt
		for i in xrange(64):
			if checkIfBothIndex0(elt[0],elt[1],i):
				dictOfIndex0[i].append(ind)
			# newAr.append(ind)

	print "\nDICTS!!"
	for key in dictOfIndex0:
		print key, dictOfIndex0[key]		
	# print dictOfIndex0
	# s = 0
	# for elt in newAr:
	# 	s += elt[2]
	# print s
	# print s/len(newAr)




