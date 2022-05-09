#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# imulogger.py : A simple data logger using InvenSense MPU9250
#
# Description:
#   A sample program to read MPU9250/AK8963 9DOF IMU sensor data.
#
# References:
#   https://invensense.tdk.com/download-pdf/mpu-9250-datasheet/
#   https://invensense.tdk.com/download-pdf/mpu-9250-register-map/
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2022/05/08 v0.1 Initial version
#
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
# TODO:
#   * write README.md
#   * write data reader/analyzer
#
import sys
import os
import time
import struct
import smbus
import yaml
import argparse

import threading
import queue

import subprocess
from subprocess import PIPE
#
# timestamp(ns): 8 bytes 
# MPU9250 Accel/Gyro/Temp raw data: 14 bytes
# In total, 8 + 14 = 22 bytes.
RECORD_SIZE = 22
#
#
cmd = None
#
#
def sample(max_count, q):
    ts_start = time.time_ns()
    print('%d : sample(): max_count: %d' % (ts_start, max_count))
    I2CBUS=1
    i2c = smbus.SMBus(I2CBUS)
    # MPU9250 i2c address
    addr_imu = 0x68
    # AK8963 i2c address
    addr_mag = 0x0c
    # Enable MPU9250
    result = i2c.write_byte_data(addr_imu, 0x6b, 0x00)

    data_total = bytearray()
    for count in range(0, max_count):
        ts = time.time_ns()
        data = bytes(i2c.read_i2c_block_data(addr_imu, 0x3b, 14))
        data_total.extend(ts.to_bytes(8, 'big'))
        data_total.extend(data)

    ts_end = time.time_ns()
    print('%d : sample(): samples: %d duration: %d (ns)' %
          (ts_end, max_count, (ts_end - ts_start)))
    
    q.put({"ts": ts_start, "payload": data_total})
    
    return

def save_thread(q):

    while True:
        msg = q.get()
        ts_begin = time.time_ns()
        if 'quit' in msg.keys() and msg['quit']:
            return
        ts_payload = msg['ts']
        data_total = msg['payload']

        output_filename = "zero1-imu-%s.bin" % ts_payload
        with open(output_filename , "ab") as wfp:
            wfp.write(data_total)
        print('%d : save_thread(): saved to: %s' % (ts_begin, output_filename))

        # example of persistent (and large) storage space.
        # rewrite below as you like.

        if args.command:
            save_cmd = args.command + ' ' + output_filename
            proc = subprocess.run(save_cmd, shell=True, stdout=PIPE,
                                  stderr=PIPE, text=True)
            ts_end = time.time_ns()
            print('%d : save_thread(): %s: exit: %d duration: %d (ns) ' % (ts_end, save_cmd, proc.returncode, (ts_end - ts_begin)))
            if proc.returncode > 0:
                print('%d : stdout %s : stderr: %s' % (ts_end, proc.stdout, procstderr))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='imulogger.py')
    parser.add_argument('-c', '--command', default=None)
    parser.add_argument('-i', '--interval', default=2000000)
    args = parser.parse_args()


    q = queue.Queue()
    th = threading.Thread(target=save_thread, args=(q,))
    th.start()
    
    poll_count = int(args.interval) # save interval (in polling count)
    print('# IMU data logger. poll_count = %d' % (poll_count))
    while True:
        sample(poll_count, q)

    q.put({'quit': True})
    th.join()
