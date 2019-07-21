"""
Work with BMP180 barometric pressure sensor

For the ESP32, the upper left pins are 3.3V, gnd, D15, D2, D4
D15 is input-only, so use D4 for SCL

BMP180   ESP32
------   -----
VIN      3V3
GND      GND
         D15  (not used)
SCL      D2
SDA      D4

"""

import machine
#
from mp_bmp180.bmp180 import BMP180
import time


BMP180_I2CADDR = 0x77

# Using the parallel wires listed at the top of this file
scl = machine.Pin(2, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
sda = machine.Pin(4, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP)
i2c = machine.I2C(scl=scl, sda=sda, freq=100000)

print("I2C scan:",", ".join(["{:2x} ".format(addr) for addr in i2c.scan()]))
# bmp = bme280.BME280(mode=bme280.BME280_OSAMPLE_1,
#                     address=BMP180_I2CADDR,
#                     i2c=i2c)

bmp = BMP180(i2c_bus=i2c)

def showBMP180(n=20, delay=1.0):
    for i in range(n):
        time.sleep(delay)
        bmp.blocking_read()
        print("T={:5.2f} C, P={:7.3f} kPa, alt={:6.1f} m".format(bmp.temperature, bmp.pressure, bmp.altitude))

showBMP180()
