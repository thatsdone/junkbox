#!/usr/bin/python3
#
# example_mpu9250.py : A sample program to read InvenSense MPU9250
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
# History:
#   * 2021/04/30 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
import smbus
import struct

I2CBUS=1
i2c = smbus.SMBus(I2CBUS)

# MPU9250 i2c address
addr_imu = 0x68
# AK8963 i2c address
addr_mag = 0x0c

# Enable MPU9250
result = i2c.write_byte_data(addr_imu, 0x6b, 0x00)
# Enable AK8963
result = i2c.write_byte_data(addr_imu, 0x37, 0x02)

data = i2c.read_byte_data(addr_imu, 0x75)
print('MPU9250 who_am_i at 0x%02x is 0x%02x (%d)' % (addr_imu, data, data))

data = i2c.read_byte_data(addr_mag, 0x00)
print('AK8963 who_am_i at 0x%02x is 0x%02x (%d)' % (addr_mag, data, data))

#
# MPU9250
#
result = i2c.read_byte_data(addr_imu, 0x1c)
print('accel config(0x1c) = 0x%02x' % (result))
result = i2c.read_byte_data(addr_imu, 0x1d)
print('accel config(0x2d) = 0x%02x' % (result))

# read 14bytes from ACCEL_XOUT_H(0x3b) - ACC(x/y/z)/TEMP/GYRO(x/y/z)
data = bytes(i2c.read_i2c_block_data(addr_imu, 0x3b, 14))

# resolution
accel_res = 2**15 / 2

# accelration/temperature/gyro are 'big endian'
accel_x = struct.unpack_from('>h', data, offset=0)[0] / accel_res
accel_y = struct.unpack_from('>h', data, offset=2)[0] / accel_res
accel_z = struct.unpack_from('>h', data, offset=4)[0] / accel_res

temp= struct.unpack_from('>h', data, offset=6)[0]
# See both Datasheet and Register Map for
temp = (temp - 21.0) / 333.87 + 21

gyro_res = 2**15 / 250
gyro_x = struct.unpack_from('>h', data, offset=8)[0] / gyro_res
gyro_y = struct.unpack_from('>h', data, offset=10)[0] / gyro_res
gyro_z = struct.unpack_from('>h', data, offset=12)[0] / gyro_res

# The below also works for one shot byte swap.
# unpacked = struct.unpack('>hhhhhhh', data[0:14])

#print('ACCEL x/y/z = %x  / %x / %x' % (accel_x, accel_y, accel_z))
print('ACCEL x/y/z = %f / %f / %f' % (accel_x, accel_y, accel_z))
print('TEMP = %f ' % (temp))
print('GYRO x/y/z = %f / %f / %f' % (gyro_x, gyro_y, gyro_z))

#
# AK8963 
#
# Enable  AK8963
#AK8963_8HZ = 0x02
#AK8963_16BIT = (0x01 << 4)
#AK8963_CNTL1 = 0x0A
result = i2c.write_byte_data(addr_mag, 0x0a, ((0x01 << 4) | 0x02))
result = i2c.write_byte_data(addr_mag, 0x0c, 0x00)

# read data x/y/z
data = bytes(i2c.read_i2c_block_data(addr_mag, 0x03, 6))

mag_res = 2**15 / 4800

# AK8963(magnetization) returns 'little endian' data
mag_x = struct.unpack_from('<h', data, offset=0)[0] / mag_res
mag_y = struct.unpack_from('<h', data, offset=2)[0] / mag_res
mag_z = struct.unpack_from('<h', data, offset=4)[0] / mag_res

print('MAG x/y/z = %f / %f / %f' % (mag_x, mag_y, mag_z))

# read status
data = i2c.read_word_data(addr_mag, 0x09)

i2c.close()

