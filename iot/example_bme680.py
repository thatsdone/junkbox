#!/usr/bin/env python
#
# example_bme686.py : A sample program to read Bosch BME680
#
# Description:
#   A sample program to read BME680 using Pimoroni bme680-python library.
#   Install bme680 using 'pip install bme680 before execution.
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
#   * 2021/12/04 v0.1 Initial version
# Authour:
#   Masanori Itoh <masanori.itoh@gmail.com>
#
import bme680
import time
#
#
# check your BME680 I2C address using i2cdetect.
# PRIMARY=0x76, SECONDARY=0x77
#bme680_addr = bme680.I2C_ADDR_PRIMARY
bme680_addr = bme680.I2C_ADDR_SECONDARY


sensor = bme680.BME680(bme680_addr)

#
# BME680 oversampling configuration
#
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
#
# IIR low pass Filter coefficient for temperature and pressure
# Valid values: 0/1/3/7/15/31/63/127
# See 'BME680 - Datasheet' rev 1.3, 3.3.4 and 5.3.2.4 	
sensor.set_filter(bme680.FILTER_SIZE_3)

#
# Enable and configure gas sensor
#
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Output format:
# timestamp temperature(celsius) pressure(hPa) humidity(%) heat(0/1) gas_registance(Ohm)
# Note(1): When heat is 0, gas_registance is meaningless.
# Note(2): When get_sensor_data() returned None, just timestamp is printed.
#
while True:
    ts = time.time()
    if sensor.get_sensor_data():
        outstr = '%f %f %f %f %d %f' % (ts,
                sensor.data.temperature,
		sensor.data.pressure,
                sensor.data.humidity,
                sensor.data.heat_stable, sensor.data.gas_resistance)
        print(outstr)
    else:
        print(ts) 
    time.sleep(1)
