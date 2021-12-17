#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# PyAudio example: Record a few seconds of audio and save to a WAVE file.
# Based on the example available at:
#   https://www.programcreek.com/python/example/52624/pyaudio.PyAudio
#
import sys
import getopt

import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"


def record(filename, duration=5):

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


if __name__ == "__main__":

    filename = 'output.wav'
    duration = 5

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:d:r:")
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

    print('duration: %d (s)' % (duration))
    record(filename, duration=10)
