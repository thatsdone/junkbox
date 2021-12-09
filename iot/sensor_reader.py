#!/usr/bin/python3
#
# SensorReader : Base class for various IoT sensor reader classes
#
# Description:
#   Base class for various IoT sensor reader classes
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2021/12/05 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
class SensorReader:

    def get_info(self):
        info = {'name': 'SensorReader base class',
                'vendor': 'some vendor',
                'sensor': 'some censor',
                'count': 2,
                'bus_type': 'i2c',
                'bus_addresses': [0x01, 0x02],
                'metrics': ['metrics1', 'metrics2'],
                'dependency': ['smbus', 'struct'],
        }
        return info

    def read_data(self):
        return dict()

if __name__ == "__main__":
    reader = SensorReader()
    print(reader.get_info())
    print(reader.read_data())

