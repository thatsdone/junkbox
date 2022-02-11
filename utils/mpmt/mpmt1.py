#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# mpmt1.py: A stupid simple example of Python threading and multiprocessing.
# By specifying '-m t' (threading) or '-m p' (multiprocessing), you can see
# cpu usage rate are different. In case threading, at most 100%, but
# in case multiprocessing you can consume as much number of cpus available.
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2021/12/20 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TOTO:
#   * Add HELP messages.
import time
import threading
import multiprocessing
import os
import sys
import getopt

def busy_worker(identity, duration):
    print('busy_worker: %d' % (identity))
    ts_orig = time.time()
    while True:
        #time.sleep(0)
        ts = time.time()
        if (ts - ts_orig > duration):
            return

if __name__ == "__main__":

    num_context = 4
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
            w = threading.Thread(target=busy_worker, args=(i, duration))
            w.setName('busy_worker/%d' % (i))
        else:
            w = multiprocessing.Process(target=busy_worker, args=(i, duration))

        workers.append(w)
        w.start()

    for w in workers:
        w.join()
        print('join: %s %s' % (w.getName(), w))
