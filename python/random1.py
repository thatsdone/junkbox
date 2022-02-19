#!/usr/bin/python3
#
# random1.py : An exercise script on random number generation/manipulation.
#
# Description:
#   An exercise to drow histogram as ASCII art and using python random number
#   generator.
#   https://stackoverflow.com/questions/38273353/how-to-repeat-individual-characters-in-strings-in-python/38273369
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2013/03/18 v0.1 Initial version
#   * 2022/02/19 v0.2 update to Python3 and use numpy
#
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * gamma
#   * dirichlet
#   * ...
#import random
import sys
import numpy as np
from scipy import stats as st

#from numpy.random import default_rng
#rng = default_rng()
#  random.normal -> standard_normal

def draw_hist(hist, column_width=50):
    elm_max = np.ceil(max(hist[0]))
    elm_min = np.ceil(min(hist[0]))
    nbins=len(hist[1]) - 1
    step=hist[1][1] - hist[1][0]
    print('==================')
    for i in range(0, nbins):
        print('%8.2f - %8.2f : %s' %
              (float(hist[1][i]),
               float(hist[1][i]+step),
               ''.join(map(lambda x: x *
                           int(np.ceil(hist[0][i] * column_width / elm_max)), "*"))))
    print('------------------')


if __name__ == "__main__":
    count = 10000
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
    print('random1.py: random number genreration and histgoram sample')
    print('count = %d' % (count))

    #normal
    avg = 5
    stddev = 1
    rand_normal  = np.zeros(count, dtype=np.float64)

    #uniform
    low = 0
    high = 10
    rand_uniform = np.zeros(count, dtype=np.float64)

    #exponential
    scale = 2.0
    size = 10
    rand_exponential = np.zeros(count, dtype=np.float64)

    #weibull
    a = 1.5      # shape : k
    size = 1     # scale : lambda
    rand_weibull = np.zeros(count, dtype=np.float64)
    
    for i in range(count):
        rand_normal[i] = np.random.normal(loc=avg, scale=stddev)
        rand_uniform[i] = np.random.uniform(low=low, high=high)
        rand_exponential[i] = np.random.exponential(scale=scale)
        rand_weibull[i] = np.random.weibull(a=a, size=size)
        
    print('normal    : avg = %f stdev = %f' % (avg, stddev))
    hist_normal = np.histogram(rand_normal, bins=20, range=(0,10))
    draw_hist(hist_normal)

    print('uniform   : low = %f high  = %f' % (low, high))
    hist_uniform = np.histogram(rand_uniform, bins=20,range=(0,10))
    draw_hist(hist_uniform)

    #print(rand_exponential)
    print('exponential : scale (1/lambda) = %f' % (scale))
    hist_exponential = np.histogram(rand_exponential, bins=20, range=(0,10))
    draw_hist(hist_exponential)

    #print(rand_weibull)
    print('weibull : k= %f lambda= = %f' % (a, size))
    hist_weibull = np.histogram(rand_weibull, bins=20, range=(0,10))
    draw_hist(hist_weibull)
