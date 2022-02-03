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
# TOTO:
#   * Make message size configurable.
import time
import threading
import queue
import multiprocessing
import os
import sys
import getopt

def pingpong_worker(identity, duration, q):
    print('pingpong_worker: %d' % (identity))
    ts_orig = time.time()
    q.put('READY')
    count = 0
    while True:
        count = count + 1
        ts = time.time()
        msg = q.get()
        #print('pingpong_worker: %s' % (msg))
        if (ts - ts_orig > duration):
            q.put('FINISH')
            print('pingpong_worker: count: %d trans/s: %.2f' % (count, count / (ts - ts_orig)))
            return
        else:
            q.put(msg)

if __name__ == "__main__":

    num_context = 1
    duration = 5
    use_thread = 1 # 1: threading, 0: multiprocessing

    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:d:m:")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for o, a in opts:
        if o == '-n':
            num_context = int(a)
        elif o == '-d':
            duration = int(a)
        elif o == '-m':
            if a == 't' or a == 'T':
                use_thread = 1
            elif a == 'p' or a == 'P':
                use_thread = 0

    print('num_context: %d, duration; %d, mode: %s' %
          (num_context, duration, 'threading' if use_thread else 'multiprocessing'))

    workers = []
    for i in range(0, num_context):
        print('creating worker: %d (mode: %s)' % (i, 'thread' if use_thread else 'process'))
        if use_thread:
            q = queue.Queue()
            w = threading.Thread(target=pingpong_worker, args=(i, duration, q))
        else:
            q = multiprocessing.Queue()
            w = multiprocessing.Process(target=pingpong_worker, args=(i, duration, q))
        workers.append(w)
        w.start()

        msg = q.get()
        #print('DEBUG: main: received %s' % (msg))
        msg = 'a'
        print('message size: %d' % len(msg))
        while True:
            q.put(msg)
            msg =q.get()
            if msg == 'FINISH':
                #print('DEBUG: received %s' % (msg))
                break

    for w in workers:
        w.join()
        print(w)
