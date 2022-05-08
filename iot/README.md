# junkbox/iot

This directory contains simple implementations for reading various
sensors connected to IoT devices, typically Raspberry Pi.

'zero_exporter.py' is a very simple Prometheus Exporter requiring only
Python standard 'http' module. Initlally written for Raspberry Pi Zero W.

## Files

* Sensor data reader modules
  * sensor_reader.py
    * Base class for individual sensor reader implementations.
  * bme680_reader.py
    * Bosch BME680 reader.
    * Temperature, Humidity, Pressure and GAS resistance
    * Depends on PyPI 'bme680' by pimoroni
  * mpu9250_reader.py
    * InvenSense MPU9250 reader.
    * Accelerometer, Gyroscope, Magnetometer and (chip) Temperature
    * Depends on PyPI 'smbus'
  * lsm9ds1_reader.py
    * STM LSM9DS1 reader.
    * Accelerometer, Gyroscope, Magnetometer and (chip) Temperature
    * Depends on 'sense-hat' for RaspberryPi
* Prometheus Exporter
  * zero_exporter.py
    * A simple Prometheus Exporter using implementations of sensor_reader.
* Examples for raw/cooked sensor data access
  * example_bme680.py
    * Example how to use bme680 library. Requires bme680 via pip.
  * example_mpu9250.py
    * Example how to use read MPU9250 sensor data using
      SMBus(I2C). Requires smbus via pip.
* Examples for data logging
  * imulogger.py
    * A simple IMU data logger for MPU9250

## TODO
* Add TI INA226 support - Current and Voltage
* Add Bosch BME280 support - Humidity, Temperature and Pressure
* Add STM HTS221 support (RaspberryPi SenseHAT) - Humidity and Temperature
* Add STM LPS25H support (RaspberryPi SenseHAT) - Pressure
* MQTT based AWS IoT Core agent (alternative of zero_exporter.py)

## Usage

1. Install necessary modules (e.g., smbus) via pip (or distro dependent package managers)
2. Execute zero_exporter.py (as background by defining systemd service for example if necessary)

### zero_exporter.py options
    * -p PORT (default: 18083)
    * -b BIND_ADDRESS (default: 0.0.0.0)
    * -s sensor1[,sensor2...] (deafault: bme680,mpu9250)
      * For now, bme680, mpu9250 and lsm9ds1 are supported.

### Scraping result

Access to the waiting URL by curl.

```
$ curl http://zero1:18083/metrics
raspi_zero_hwmon{raspi="zero1",hwmon="hwmon0",name="cpu_thermal"} 31.476000
raspi_zero_sensor{raspi="zero1",sensor="BME680",metric="temperature"} 18.84
raspi_zero_sensor{raspi="zero1",sensor="BME680",metric="pressure"} 1016.51
raspi_zero_sensor{raspi="zero1",sensor="BME680",metric="humidity"} 73.68
raspi_zero_sensor{raspi="zero1",sensor="BME680",metric="heat_stable"} 0
raspi_zero_sensor{raspi="zero1",sensor="BME680",metric="gas_resistance"} 93546.65170365213
raspi_zero_sensor{raspi="zero1",sensor="MPU9250",metric="acc_x"} 0.017822265625
raspi_zero_sensor{raspi="zero1",sensor="MPU9250",metric="acc_y"} 0.02392578125
raspi_zero_sensor{raspi="zero1",sensor="MPU9250",metric="acc_z"} 1.018798828125
raspi_zero_sensor{raspi="zero1",sensor="MPU9250",metric="temp"} 23.045706412675592
raspi_zero_sensor{raspi="zero1",sensor="MPU9250",metric="gyr_x"} 0.17547607421875
raspi_zero_sensor{raspi="zero1",sensor="MPU9250",metric="gyr_y"} 0.17547607421875
raspi_zero_sensor{raspi="zero1",sensor="MPU9250",metric="gyr_z"} 0.69427490234375
raspi_zero_sensor{raspi="zero1",sensor="MPU9250",metric="mag_x"} -31.494140624999996
raspi_zero_sensor{raspi="zero1",sensor="MPU9250",metric="mag_y"} 24.462890625
raspi_zero_sensor{raspi="zero1",sensor="MPU9250",metric="mag_z"} 5.712890625
$
```

