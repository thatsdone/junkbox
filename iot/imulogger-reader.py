#!/usr/bin/python3
#
# imulogger-reader.py : A sample program to read InvenSense MPU9250
#
# Description:
#   A tiny utility for analyzing data saved by imulogger.py
#
# References:
#   https://invensense.tdk.com/download-pdf/mpu-9250-datasheet/
#   https://invensense.tdk.com/download-pdf/mpu-9250-register-map/
#
# License:
#   Apache License, Version 2.0
#
# History:
#   * 2022/05/21 v0.1 Initial version
#
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
import sys
import os
import time
import struct
import numpy as np
from scipy import stats as st
import argparse
import datetime


RECORD_SIZE = 22

start_ts = 0
end_ts = 0


def show_data(args):

    reader(args)
    return

#def show_interval(args):
#    reader(args)

def extract_one(data):
    offset = 8
    # resolution
    accel_res = 2**15 / 2
    # accelration/temperature/gyro are 'big endian'
    accel_x = struct.unpack_from('>h', data, offset=offset+0)[0] / accel_res
    accel_y = struct.unpack_from('>h', data, offset=offset+2)[0] / accel_res
    accel_z = struct.unpack_from('>h', data, offset=offset+4)[0] / accel_res

    temp= struct.unpack_from('>h', data, offset=offset+6)[0]
    # See both Datasheet and Register Map for MPU9250
    # Note that MPU6000 series has different constants.
    temp = (temp - 21.0) / 333.87 + 21

    gyro_res = 2**15 / 250
    gyro_x = struct.unpack_from('>h', data, offset=offset+8)[0] / gyro_res
    gyro_y = struct.unpack_from('>h', data, offset=offset+10)[0] / gyro_res
    gyro_z = struct.unpack_from('>h', data, offset=offset+12)[0] / gyro_res

    return accel_x, accel_y, accel_z, temp, gyro_x, gyro_y, gyro_z


def show_data_one(data):

    ts = struct.unpack_from('>Q', data, offset=0)[0]
    #tss = datetime.datetime.fromtimestamp(ts/1000/1000/1000)
    
    (accel_x, accel_y, accel_z, temp, gyro_x, gyro_y, gyro_z) =  extract_one(data)
    print('%s %f %f %f %f %f %f %f' % (ts, accel_x, accel_y, accel_z, temp,
                                       gyro_x, gyro_y, gyro_z))

    return


def show_stats(args):

    datafile = args.datafile
    outlier_factor = 5
    print('# analyzing %s outside %d sigma' % (datafile, outlier_factor))
    
    with open(datafile, "rb") as rfp:
        data = rfp.read(RECORD_SIZE)
        filesize = os.fstat(rfp.fileno()).st_size
        print('# file size: %d num_records(%d): %d' % (filesize, RECORD_SIZE, filesize / RECORD_SIZE))

        num_rows = int(filesize / RECORD_SIZE)
        data_array = np.zeros((num_rows, 8), dtype=np.float64)
        
        count = 0
        while data:
            ts = struct.unpack_from('>Q', data, offset=0)[0]
            tss = datetime.datetime.fromtimestamp(ts/1000/1000/1000)
            if ts < start_ts:
                #print('skipping: %d %d (%s) %d' % (start_ts, ts, tss, end_ts))
                data = rfp.read(RECORD_SIZE)            
                continue
            if args.end and ts > end_ts:
                return
            (accel_x, accel_y, accel_z,
             temp,
             gyro_x, gyro_y, gyro_z) =  extract_one(data)
            a = np.array([ts,
                          accel_x,
                          accel_y,
                          accel_z,
                          gyro_x,
                          gyro_y,
                          gyro_z,
                          temp],
                         dtype=np.float64)
            data_array[count] = a
            count += 1
            data = rfp.read(RECORD_SIZE)
           
    desc = st.describe(data_array)
    print('# scipy.stats.describe result.')
    print(desc)
    axis = ['ts', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'temp']
    for i in range(1, 4):
        mean =desc[2][i]
        sigmax = np.sqrt(desc[3][i]) * outlier_factor
        minimum = desc[1][0][i]
        maximum = desc[1][1][i]
        if minimum < mean - sigmax:
            print('# minimum outlier: %s %f %f %f' % (axis[i], mean, minimum, mean - sigmax))
        if maximum > mean + sigmax:
            print('# maximum outlier: %s %f %f %f' % (axis[i], mean,maximum, mean + sigmax))
    
    return
    
def reader(args): #, method=None):
    
    method=show_data_one

    datafile = args.datafile

    with open(datafile, "rb") as rfp:
        data = rfp.read(RECORD_SIZE)
        filesize = os.fstat(rfp.fileno()).st_size
        print('# file size: %d num_records(%d): %d' % (filesize, RECORD_SIZE, filesize / RECORD_SIZE))
        ts_save = struct.unpack_from('>Q', data, offset=0)[0]
        while data:
            ts = struct.unpack_from('>Q', data, offset=0)[0]
            if ts < start_ts:
                data = rfp.read(RECORD_SIZE)            
                continue
            if args.end and ts > end_ts:
                return

            method(data)

            ts_save = ts
            data = rfp.read(RECORD_SIZE)
#
#
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='imulogger-reader.py')
    parser.add_argument('-f', '--datafile', default=None)
    parser.add_argument('-c', '--command', default='show')
    parser.add_argument('-s', '--start', default=None)
    parser.add_argument('-e', '--end', default=None)
    #parser.add_argument('-q', '--query', default=None)
    args = parser.parse_args()

    if args.start:
        print('# start: ', args.start)
        start = datetime.datetime.strptime(args.start, '%Y/%m/%d %H:%M:%S')
        start_ts = datetime.datetime.timestamp(start) #+ 9 * 3600
        start_ts = start_ts * 1000 * 1000 * 1000
    if args.end:
        print('# end:   ', args.end)
        end = datetime.datetime.strptime(args.end, '%Y/%m/%d %H:%M:%S')
        end_ts = datetime.datetime.timestamp(end) #+ 9 * 3600
        end_ts = end_ts * 1000 * 1000 * 1000
    
    if not args.datafile:
        print('specify a datafile')
        sys.exit()

    if args.command == 'show' or args.command == 'show_interval':
        show_data(args)
    elif args.command == 'stats':
        show_stats(args)
    elif args.command == 'show_interval':
        show_interval(args)
