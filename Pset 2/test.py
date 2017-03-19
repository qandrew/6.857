# test

from multiprocessing import Pool

c = 132

def isgood(a):
	return a

pool = Pool()

result1 = pool.apply_async(isgood, [123])    # evaluate "solve1(A)" asynchronously
result2 = pool.apply_async(isgood, [1])    # evaluate "solve2(B)" asynchronously
answer1 = result1.get(timeout=10)
answer2 = result2.get(timeout=10)
result1 = pool.apply_async(isgood, [1231])    # evaluate "solve1(A)" asynchronously
answer1 = result1.get(timeout=10)
answer2 = result2.get(timeout=10)


print answer1,answer2

results = []

s = 1

for i in xrange(10):
		results.append(pool.apply_async(isgood, [s]))
		s += 1

while True:
	
	for i in xrange(10):
		x = results[i].get(timeout=10)
		print 'rec',x
		if x == c:
			print 'fuck'
			break

	for i in xrange(10):
		results[i] = pool.apply_async(isgood, [s])
		s += 1
		print 'snd', s

	if s > 200:
		break

print 'done'