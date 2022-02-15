import sys
import numpy as np
from scipy import stats as st


if len(sys.argv) > 1:
    avg = float(sys.argv[1])
else:
    avg = 30.0

if len(sys.argv) > 2:
    stddev = float(sys.argv[2])
else:
    stddev = avg / 10.0

count=10000

darray = np.zeros(count, dtype=np.float32)

print('avg: %f stddev: %f count: %d' % (avg, stddev, count))
for i in range(0, count):
    darray[i] = np.random.normal(loc=avg, scale=stddev)
    #darray[i] = np.random.uniform(low = (avg - stddev), high = (avg + stddev))
    #print(darray[i])

print(st.describe(darray))

