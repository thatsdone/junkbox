#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pyaudio1.py: A simple example to read microphone data and save it
# as an WAVE file using PyAudio and Scipy.
# Based on the example available at:
#   https://www.programcreek.com/python/example/52624/pyaudio.PyAudio
# But, significantly rewritten.
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2021/12/18 v0.1 Initial version based on:
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TOTO:
#   * Add HELP messages.
#
import sys
import getopt
import time

import pyaudio
import wave

import scipy
from scipy import stats as st
from scipy.io.wavfile import write as scipy_write
import numpy as np

debug = False


def record(filename, duration=5, rate=44100, fps=20, format=pyaudio.paInt32, channels=1):

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    if debug:
        print("DEBUG: mic polling start")

    frames = []
    num_loop = int(rate / chunk * duration)
    if debug:
        print('DEBUG: num_loop = %d' % (num_loop))

    ts_save = time.time_ns()
    for i in range(0, num_loop):
        ts = time.time_ns()
        data = stream.read(chunk)
        #print('DEBUG: type: %s length : %d' % (type(data), len(data)))
        frames.append(data)
        if debug:
            print('DEBUG: poll duration: %f (ms)' % ((ts - ts_save)/1000/1000))
        ts_save = ts
    if debug:
        print("DEBUG: mic polling done")

    stream.stop_stream()
    stream.close()
    p.terminate()

    buf = b''.join(frames)
    ndata = np.frombuffer(buf, dtype='int32')
    if debug:
        print('DEBUG: shape: %s ' % (ndata.shape))
        print(scipy.stats.describe(ndata))
        #sys.exit()

    #scipy.io.wavfile.write(filename, rate, ndata.astype('int32'))
    scipy_write(filename, rate, ndata.astype('int32'))
    sys.exit()

#    wf = wave.open(filename, 'wb')
#    wf.setnchannels(channels)
#    wf.setsampwidth(p.get_sample_size(format))
#    wf.setframerate(rate)
#    wf.writeframes(buf)
#    wf.close()


if __name__ == "__main__":

    # default values
    filename = 'output.wav'
    duration = 5
    rate = 44100
    fps = 20
    chunk = (int)(rate / fps)
    format = pyaudio.paInt32
    channels = 1

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:d:r:f:F:c:D")
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for o, a in opts:
        if o == '-f':
            filename = a
        elif o == '-d':
            duration = int(a)
        elif o == '-f':
            rate = int(a)
        elif o == '-F':
            if a == 'S32_LE':
                format=pyaudio.paInt32
            elif a == 'S16_LE':
                format=pyaudio.paInt32
            else:
                printf('Unknown format: %s' % (a))
                sys.exit()
        elif o == '-f':
            # frames per sample
            fps = int(a)
        elif o == '-c':
            # channels: 1: monoral, 2: stereo
            channels = int(a)
        elif o == '-D':
            debug = True

    print('duration: %d (s)' % (duration))
    record(filename, duration=duration, rate=rate)
