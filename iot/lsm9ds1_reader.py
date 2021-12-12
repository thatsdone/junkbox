#!/usr/bin/env python
#
# lsm9ds1_reader.py : STM LSM9DS1 handler
#
# Description:
#   Handles STM LSM9DS1 sensor data based on SensorReader class.
#   Accleration, Rotation and Magnetization.
#   Currently, runs on only RaspiOS and does not return temperature.
#
# References:
#   https://www.st.com/en/mems-and-sensors/lsm9ds1.html
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2021/12/11 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * Use I2C low level access library, smbus (free from SenseHAT)
#   * Retrieve temperature from LSM9DS1
#
from sensor_reader import SensorReader
from sense_hat import SenseHat


class LSM9DS1Reader(SensorReader):
    def __init__(self):
        # Enable and initialize LSM9DS1 via sense_hat
        self.sense = SenseHat()
        self.sense.clear()

        super().__init__()
        return

    def get_info(self):
        info = {'name': type(self).__name__,
                'vendor': 'STMicroelectoronics',
                'sensor': 'LSM9DS1',
                'count': 1,  # up to 2, need auto detection.
                'bus_type': 'i2c',
                'bus_addresses': [0x6a, 0x1c],  # canbe 0x6b, 0x1e
                'metrics': ['acc_x', 'acc_y', 'acc_z',
                            'gyr_x', 'gyr_y', 'gyr_z',
                            'mag_x', 'mag_y', 'mag_z'
                ],
                'dependency': ['sense-hat']
        }
        return info

    # override
    def read_data(self):
        data = dict()
        acc = self.sense.get_accelerometer_raw()
        # In case of sense-hat, STM HTS221 returns temperature.
        # temp = self.sense.get_temperature()
        gyr = self.sense.get_gyroscope_raw()
        mag = self.sense.get_compass_raw()

        data['acc_x'] = acc['x']
        data['acc_y'] = acc['y']
        data['acc_z'] = acc['z']
        data['gyr_x'] = gyr['x']
        data['gyr_y'] = gyr['y']
        data['gyr_z'] = gyr['z']
        data['mag_x'] = mag['x']
        data['mag_y'] = mag['y']
        data['mag_z'] = mag['z']

        return data


if __name__ == "__main__":

    import time
    import pprint as pp

    reader = LSM9DS1Reader()

    pp.pprint(reader.get_info())

    while True:
        ts = time.time()
        data = reader.read_data()

        if data:
            outstr = '%f %f %f %f %f %f %f %f %f %f' % (
                ts,
                data['acc_x'],
                data['acc_y'],
                data['acc_z'],
                data['gyr_x'],
                data['gyr_y'],
                data['gyr_z'],
                data['mag_x'],
                data['mag_y'],
                data['mag_z'])
            print(outstr)
        else:
            print(ts)

        time.sleep(1)
