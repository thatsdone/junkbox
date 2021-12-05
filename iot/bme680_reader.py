#!/usr/bin/env python
#
# bme680_reader.py : Bosch BME680 handler
#
# Description:
#   Handles Bosch BME680 sensor data based on SensorReader class.
#   Temperature, Pressure, Humidity and Gas resistance.
#
# References:
#   * https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme680/
#   * https://pypi.org/project/bme680/
#   * https://github.com/pimoroni/bme680-python
#   * https://en.wikipedia.org/wiki/Infinite_impulse_response   
#   * https://en.wikipedia.org/wiki/Oversampling 
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2021/12/05 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
import bme680
from sensor_reader import SensorReader

class BME680Reader(SensorReader):
    def __init__(self):
        # check your BME680 I2C address using i2cdetect.
        # PRIMARY=0x76, SECONDARY=0x77
        #self.bme680_addr = bme680.I2C_ADDR_PRIMARY
        self.bme680_addr = bme680.I2C_ADDR_SECONDARY
        self.sensor = bme680.BME680(self.bme680_addr)
        #
        # BME680 oversampling configuration
        #
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        #
        # IIR low pass Filter coefficient for temperature and pressure
        # Valid values: 0/1/3/7/15/31/63/127
        # See 'BME680 - Datasheet' rev 1.3, 3.3.4 and 5.3.2.4   
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        #
        # Enable and configure gas sensor
        #
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)

        super().__init__()
        return 

    def get_info(self):
        info = {'name': type(self).__name__,
                'vendor': 'BOSCH',
                'sensor': 'BME680',
                'count': 1, # up to 2, need auto detection.
                'bus_type': 'i2c',
                'bus_addresses': [bme680.I2C_ADDR_SECONDARY],
                'metrics': ['temperature', 'pressure', 'humidity', 'heat_stable', 'gas resitance'],
                'dependency': ['bme680']
        }
        return info
        
    # override
    def read_data(self):
        self.sensor.get_sensor_data()
        if not self.sensor.data:
            return None

        data = dict()
        data['temperature'] = self.sensor.data.temperature
        data['pressure'] = self.sensor.data.pressure
        data['humidity'] = self.sensor.data.humidity
        data['heat_stable'] = self.sensor.data.heat_stable
        data['gas_resistance'] = self.sensor.data.gas_resistance
        return data

if __name__ == "__main__":
    import time
    import pprint as pp

    # Output format:
    # timestamp temperature(celsius) pressure(hPa) humidity(%) heat_stable(0/1) gas_registance(Ohm)
    # Note(1): When heat_stable is 0, gas_registance is meaningless.
    # Note(2): When read_data() returned None, just timestamp is printed.
    #
    reader = BME680Reader()
    pp.pprint(reader.get_info())
    
    while True:
        ts = time.time()
        data = reader.read_data()
        if data:
            outstr = '%f %f %f %f %d %f' % (
                ts,
                data['temperature'],
                data['pressure'],
                data['humidity'],
                data['heat_stable'],
                data['gas_resistance'])
            print(outstr)
        else:
            print(ts) 

        time.sleep(1)
