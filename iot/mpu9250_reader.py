#!/usr/bin/env python
#
# mpu9250_reader.py : InvenSense MPU9250 handler
#
# Description:
#   Handles InvenSense MPU9250 sensor data based on SensorReader class.
#   Accleration, Rotation, Magnetization and (chip) Temperature
#
# References:
#   * https://invensense.tdk.com/download-pdf/mpu-9250-datasheet/
#   * https://invensense.tdk.com/download-pdf/mpu-9250-register-map/
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2021/12/05 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
#

import smbus
import struct
from sensor_reader import SensorReader

I2CBUS=1


class MPU9250Reader(SensorReader):
    def __init__(self):
        # check your BME680 I2C address using i2cdetect.
        # PRIMARY=0x76, SECONDARY=0x77
        self.i2c_bus = 1

        self.i2c = smbus.SMBus(I2CBUS)
        # MPU9250 i2c address
        self.addr_imu = 0x68
        # AK8963 i2c address
        self.addr_mag = 0x0c

        # Enable MPU9250
        self.i2c.write_byte_data(self.addr_imu, 0x6b, 0x00)
        # Enable AK8963
        self.i2c.write_byte_data(self.addr_imu, 0x37, 0x02)

        self.accel_res = 2**15 / 2
        self.gyro_res = 2**15 / 250

        # Configure AK8963
        #AK8963_8HZ = 0x02
        #AK8963_16BIT = (0x01 << 4)
        #AK8963_CNTL1 = 0x0A
        self.i2c.write_byte_data(self.addr_mag, 0x0a, ((0x01 << 4) | 0x02))
        self.i2c.write_byte_data(self.addr_mag, 0x0c, 0x00)
        self.mag_res = 2**15 / 4800
        
        super().__init__()
        return 

    def get_info(self):
        info = {'name': type(self).__name__,
                'vendor': 'InvenSense',
                'sensor': 'MPU9250/AK8963',
                'count': 1, # up to 2, need auto detection.
                'bus_type': 'i2c',
                'bus_addresses': [0x68], # need auto detection.
                'metrics': ['acc_x', 'acc_y', 'acc_z',
                            'temp',
                            'gyr_x', 'gyr_y', 'gyr_z',
                            'mag_x', 'mag_y', 'mag_z'
                ],
                'dependency': ['smbus', 'struct']
        }
        return info
        
    # override
    def read_data(self):
        data = dict()
        #self.sensor.get_sensor_data()
        #return self.sensor.data
        
        raw1 = bytes(self.i2c.read_i2c_block_data(self.addr_imu, 0x3b, 14))
        raw2 = bytes(self.i2c.read_i2c_block_data(self.addr_mag, 0x03, 6))
        
        # accelration/temperature/gyro are 'big endian'
        data['acc_x'] = struct.unpack_from('>h', raw1, offset=0)[0] / self.accel_res
        data['acc_y']  = struct.unpack_from('>h', raw1, offset=2)[0] / self.accel_res
        data['acc_z'] = struct.unpack_from('>h', raw1, offset=4)[0] / self.accel_res
        data['temp'] = struct.unpack_from('>h', raw1, offset=6)[0]
        # See both Datasheet and Register Map of MPU9250
        data['temp'] = (data['temp'] - 21.0) / 333.87 + 21
        data['gyr_x'] = struct.unpack_from('>h', raw1, offset=8)[0] / self.gyro_res
        data['gyr_y'] = struct.unpack_from('>h', raw1, offset=10)[0] / self.gyro_res
        data['gyr_z'] = struct.unpack_from('>h', raw1, offset=12)[0] / self.gyro_res
        #
        data['mag_x'] = struct.unpack_from('<h', raw2, offset=0)[0] / self.mag_res
        data['mag_y'] = struct.unpack_from('<h', raw2, offset=2)[0] / self.mag_res
        data['mag_z'] = struct.unpack_from('<h', raw2, offset=4)[0] / self.mag_res

        return data

if __name__ == "__main__":

    import time
    import pprint as pp

    reader = MPU9250Reader()

    pp.pprint(reader.get_info())
    
    while True:
        ts = time.time()
        data = reader.read_data()
        if data:
            outstr = '%f %f %f %f %f %f %f %f %f %f %f' % (
                ts,
                data['acc_x'],
                data['acc_y'],
                data['acc_z'],
                data['gyr_x'],
                data['gyr_y'],
                data['gyr_z'],
                data['mag_x'],
                data['mag_y'],
                data['mag_z'],
                data['temp'])
            print(outstr)
        else:
            print(ts) 

        time.sleep(1)
