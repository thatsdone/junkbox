#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# mpmt2.py: A stupid simple pingpong communication example by Python Queue.
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2022/02/03 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
import time
import threading
import queue
import multiprocessing
import os
import sys
import getopt
import random
import string
import numpy as np
from scipy import stats as st

def random_string(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

nd_max = 10000

def pingpong_worker(identity, duration, max_count, q, size):
    print('pingpong_worker: %d' % (identity))

    darray = np.zeros(nd_max, dtype=np.float32)

    ts_orig = time.time()
    ts_save = ts_orig
    q.put('READY')
    count = 0
    while True:
        ts = time.time()
        if count < nd_max:
            darray[count] = ts - ts_save
        ts_save = ts
        count = count + 1
        msg = q.get()
        #print('pingpong_worker: %s' % (msg))
        if (duration and (ts - ts_orig > duration)) or (max_count and (count >= max_count)):
            q.put('FINISH')
            print('pingpong_worker: %d bytes %d trans. %f %.2f trans./s ' % (size, count, (ts - ts_orig) ,count / (ts - ts_orig)))
            print(st.describe(darray))
            return
        else:
            q.put(msg)


if __name__ == "__main__":

    num_context = 1
    duration = 5
    use_thread = 1 # 1: threading, 0: multiprocessing
    count = 10000
    size = 1
    count_set = 0
    duration_set = 0

    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:d:m:c:s:")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for o, a in opts:
        if o == '-n':
            num_context = int(a)
        elif o == '-d':
            duration = int(a)
            duration_set = 1
            count = 0
        elif o == '-c':
            count = int(a)
            count_set = 1
            duration = 0
        elif o == '-s':
            size = int(a)
        elif o == '-m':
            if a == 't' or a == 'T':
                use_thread = 1
            elif a == 'p' or a == 'P':
                use_thread = 0

    if count_set and duration_set:
        print('-c and -d are exclusive.')
        sys.exit()

    print('num_context: %d, duration; %d, mode: %s' %
          (num_context, duration, 'threading' if use_thread else 'multiprocessing'))

    workers = []
    for i in range(0, num_context):
        print('creating worker: %d (mode: %s)' % (i, 'thread' if use_thread else 'process'))
        if use_thread:
            q = queue.Queue()
            w = threading.Thread(target=pingpong_worker, args=(i, duration, count, q, size))
        else:
            q = multiprocessing.Queue()
            w = multiprocessing.Process(target=pingpong_worker, args=(i, duration, count, q, size))
        workers.append(w)
        w.start()

        msg = q.get()
        #print('DEBUG: main: received %s' % (msg))
        msg = random_string(N=size)
        print('message size: %d' % len(msg))
        while True:
            q.put(msg)
            msg =q.get()
            if msg == 'FINISH':
                #print('DEBUG: received %s' % (msg))
                break

    for w in workers:
        w.join()
        #print(w)
