import machine
from machine import Pin, Timer
import time

led=Pin(2, Pin.OUT)

def toggleLED(timer):
    led.value(not led.value())

tim4 = Timer(4)
tim4.init(period=300, mode=machine.Timer.PERIODIC, callback=toggleLED)
time.sleep(20)
tim4.deinit()

