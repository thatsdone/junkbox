#
# An exercise script on random number generation/manipulation.
# ref. http://effbot.org/librarybook/random.htm
#
# https://stackoverflow.com/questions/38273353/how-to-repeat-individual-characters-in-strings-in-python/38273369
#
import random
import sys


print('0.0<=float<1.0 10<=float<20  100<=int<= 1000  100<=even int.< 1000')
for i in range(5):
    #print '| random float: 0.0 <= number < 1.0'
    print('%15.13f' %  random.random())
    #print('| random float: 10 <= number < 20'
    print('%16.14f' % random.uniform(10, 20))
    #print('| random integer: 100 <= number <= 1000'
    print('%5d' % random.randint(100, 1000))
    #print('| random integer: even numbers in 100 <= number < 1000'
    print('%5d' % random.randrange(100, 1000, 2))

print('')

histogram = [0] * 20 
histogram2 = [0] * 20 
for i in range(1000):
    j = int(random.gauss(5, 1) * 2)
    k = int(random.uniform(0, 10) * 2)
    histogram[j] = histogram[j] + 1
    histogram2[k] = histogram2[k] + 1

print('Generate gaussian random number sequence and show histogram picture')
m = max(histogram)
for v in histogram:
    print('| %s' % (''.join(map(lambda x: x * int(v * 50 / m), "*"))))

print('Generate uniform and gaussian random number sequences and show histogram')
for v in range(0, 20):
    print('%4.1f - %4.1f : %5d %5d' % (float(v) / 2, (float(v) + 1) / 2, histogram[v], histogram2[v]))



#random.seed()
#
#count = 0
#while True:
#    if count > 100:
#        sys.exit(0)
#    print(random()
#    print(uniform(0,10)



