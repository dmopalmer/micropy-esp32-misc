"""
Speak the time when the touch-sensitive pin is touched

Hook piezo speaker (high impedence) to a DAC pin, which on
the ESP32 DEVKIT 1 is either GPIO25 or GPIO26 (DAC1 and DAC2)


Where do voices come from?
https://evolution.voxeo.com/library/audio/prompts/numbers/index.jsp


"""

import machine
import math
import time
import connect
import ntptime
import machine

connect.do_connect(verbose=True)
ntptime.settime()

rtc = machine.RTC()


speakerpin = machine.Pin(25)

dac = machine.DAC(speakerpin)


def dacspeedtest():
    nomadcfreq = 8000
    duration = 1
    nomperiod_us = 1000000 // nomadcfreq
    nomaudiofreq = 1500
    bytes= bytearray([int(128 + 120*math.sin(math.pi * i * nomaudiofreq/nomadcfreq))
                      for i in range(int(nomadcfreq * duration))])

    for i in range(10):
        for b in bytes:
            dac.write(b)
            time.sleep_us(nomperiod_us)

