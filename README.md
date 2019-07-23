# micropy-esp32-misc
Miscellaneous bits of playing around with micro-python on the ESP32.  Not necessarily useful to anyone.


## Installing micropython on ESP32

On your Mac or Linux machine:

1\. (optional) Set up a python3 environment and enter it  (example using Anaconda)

1.1 `conda create --name esp python=3`

1.2 `source activate esp`

2\. Install python packages

2.1 `pip install adafruit-ampy`

2.2 `pip install esptool`

3\. Plug the ESP32 into your desktop and figure out what port it corresponds to.  (e.g. by diffing a listing of /dev).  Assign it to a bash environment variable so that ampy knows where to find it.  On my computer it is **/dev/cu.SLAB_USBtoUART**, but it will be different on yours. 

3.1 `export AMPY_PORT=/dev/cu.SLAB_USBtoUART`


4\. Download the latest build from http://micropython.org/download#esp32, then send it to the ESP32

4.1 `esptool.py --chip esp32 --port $AMPY_PORT write_flash -z 0x1000 /where/you/download/stuff/esp32-20171109-v1.9.2-443-g236297f4.bin`

5\. Add file containing credentials, to convert your IoT thing into a massive security breach,as is traditional. (Note that cred.txt is in the .gitignore file.)

5.1 Change all this to fit your wifi system.  Note that case is important.
```
cat - > cred.txt
wificlient:mywifi:password1
wifihost:HoneyPot:HoneyPot
```

5.2  This cred.txt file is read by the do_connect() function in connect.py.
do_connect() reads each `wificlient` line and tries to connect to the network named in the 
second field (e.g. `mywifi`) using the password in the third field (`password1`).
If there are multiple wificlient lines, it tries each one in turn until it succeeds
in signing in or it runs out of lines.

If there is a wifihost line, it also presents itself as a wifi host that you can connect
to.  The esp32 is at 192.168.4.1 on that network.

do_connect() is called by the main.py script, which is executed when the process boots.


5.3 Then upload the relevant files
``` 
ampy put cred.txt
ampy put connect.py
ampy put main.py
```

5.4

If you go to the repl via the serial port:
```
screen $AMPY_PORT 115200
```
Then you can reboot the esp32
```
import machine
machine.reset()
```
and it will tell you with lines like:
```
I (4327) network: CONNECTED
I (6647) event: sta ip: 192.168.1.113, mask: 255.255.255.0, gw: 192.168.1.1
I (6647) network: GOT_IP
```
what IP address it is using on wifi.  (In this case 192.168.1.113).

5.5

Onee you have a network connection, you can use the webrepl (instructions:
https://docs.micropython.org/en/latest/esp32/quickref.html#webrepl-web-browser-interactive-prompt  
) to talk to it over the network without using the serial port.

## Using micropython and these misc things

### Set up environment
```
source activate esp
export AMPY_PORT=/dev/cu.SLAB_USBtoUART
```
### Try the REPL:

```
screen $AMPY_PORT 115200
>>>
```

(ctrl-A, ctrl-\ to get out of screen)

### Run a test script (blinking the pin2 LED on ESP32 Devkit V1)

```
ampy run blink.py
```
