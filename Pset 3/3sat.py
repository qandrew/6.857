# generate 3sat stuff
# Andrew Xia
# 6.857 pset 3
# March 19 2017

import random

from satispy import Variable, Cnf
from satispy.solver import Minisat

global k
k = 10
global e #expression count
e = 4

def genKey():
	# return random.getrandbits(k)

	# return 2**256-1 #since we want all 1s

	variables = [Variable(str(i)) for i in xrange(k)] #all the 3sat variables
	return "1"*k, variables

def genRandomClauses(num,key):
	clauses = ""

	# choices = range(8)
	# print choices

	for i in xrange(num):
		# first, get 3 random numbers
		x = random.randrange(k)
		y = random.randrange(k)
		z = random.randrange(k)
		print "x,y,z",x,y,z, "keys", key[x], key[y], key[z]
		# let the options be the binary expansion 
		# of the random numbers that we are generating

		cant = 1-int(key[x])
		cant2 = 1-int(key[y])
		cant3 = 1-int(key[z])
		cantStr = str(cant) + str(cant2) + str(cant3)

		choices = range(8)
		choices.remove(int(cantStr,2))

		selected = random.choice(choices) #the clause we want
		selectedBin = '{0:03b}'.format(selected)

		print cantStr, choices, selectedBin

		# add to clause
		clause = "( "
		if selectedBin[0] == "0":
			clause += "-"+str(x)
		else: 
			clause += str(x)

		clause += " | "

		if selectedBin[1] == "0":
			clause += "-"+str(y)
		else: 
			clause += str(y)

		clause += " | "

		if selectedBin[2] == "0":
			clause += "-"+str(z)
		else: 
			clause += str(z)

		clause += " ) & "

		clauses += clause

	return clauses[:-3]

def genRandomClauses2(num,key):
	clauses = []

	# choices = range(8)
	# print choices

	for i in xrange(num):
		# first, get 3 random numbers
		x = random.randrange(k)
		y = random.randrange(k)
		z = random.randrange(k)
		# print "x,y,z",x,y,z, "keys", key[x], key[y], key[z]
		# let the options be the binary expansion 
		# of the random numbers that we are generating

		cant = 1-int(key[x])
		cant2 = 1-int(key[y])
		cant3 = 1-int(key[z])
		cantStr = str(cant) + str(cant2) + str(cant3)

		choices = range(8)
		choices.remove(int(cantStr,2))

		selected = random.choice(choices) #the clause we want
		selectedBin = '{0:03b}'.format(selected)

		clause = ''
		# add to clause
		if selectedBin[0] == "0":
			clause += "-"+str(x)
		else: 
			clause += str(x)

		clause += " "

		if selectedBin[1] == "0":
			clause += "-"+str(y)
		else: 
			clause += str(y)

		clause += " "

		if selectedBin[2] == "0":
			clause += "-"+str(z)
		else: 
			clause += str(z)

		clauses.append(clause)

	return clauses

if __name__ == "__main__":
	key, variables = genKey()

	exp = genRandomClauses2(e,key)

	print "p cnf", k, e
	for row in exp:
		print row

	# v1 = Variable('v1')
	# v2 = Variable('v2')
	# v3 = Variable('v3')

	# var = []
	# for i in xrange(k):
	# 	var.append(Variable(str(i)))

	# exp = v1 & v2 | v3

	# solver = Minisat()

	# solution = solver.solve(exp)

	# if solution.success:
	#     print "Found a solution:"
	#     # for i in xrange(k):
	#     # 	print i,solution[key[i]],
	# else:
	#     print "The expression cannot be satisfied"
