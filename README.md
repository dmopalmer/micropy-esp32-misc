# micropy-esp32-misc
Miscellaneous bits of playing around with micro-python on the ESP32.  Not necessarily useful to anyone.


## Installing micropython on ESP32

On your Mac or Linux machine:

1. (optional) Set up a python3 environment and enter it  (example using Anaconda)

1.1. % conda create --name esp python=3

1.2. % source activate esp

2. Install python packages

2.1. % pip install adafruit-ampy

2.2. % pip install esptool

3. Plug the ESP32 into your desktop and figure out what port it corresponds to.  (e.g. by diffing a listing of /dev).  Assign it to a bash environment variable so that ampy knows where to find it.

3.1. % export AMPY_PORT=/dev/cu.SLAB_USBtoUART

4. Grab the latest build from http://micropython.org/download#esp32 and download it to the ESP32

4.1. esptool.py --chip esp32 --port $AMPY_PORT write_flash -z 0x1000 <where you download stuff>/esp32-20171109-v1.9.2-443-g236297f4.bin

5. Add file containing credentials, to convert your IoT thing into a massive security breach,as is traditional:

5.1. Note that cred.txt is in the .gitignore file

5.2. 
```
cat - > cred.txt
wificlient:mywifi:password1
wifihost:HoneyPot:HoneyPot
```

5.3. ampy put cred.txt


## Using micropython and these misc things

### Set up environment

source activate esp
export AMPY_PORT=/dev/cu.SLAB_USBtoUART

### Try the REPL:

screen $AMPY_PORT 115200
>>>
(ctrl-A, ctrl-\ to get out of screen)

### Run a test script (blinking the pin2 LED on ESP32 Devkit V1)

ampy run blink.py
