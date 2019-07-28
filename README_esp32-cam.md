# Special instructions for ESP32-CAM

You can get ESP32 modules which include cameras.
https://makeradvisor.com/tools/esp32-cam/


These do not have the USB-serial converter onboard.
You need an FTDI or equivalent to program them.
The FTDI must be set to 3.3V or it will burn out the pins on the ESP32.

You can use either Arduino or Micropython to program them.

A description of how to program them with Arduino is at
https://randomnerdtutorials.com/esp32-cam-video-streaming-face-recognition-arduino-ide/

Powering them with 3.3V tends to cause problems so, the wiring I use is:

| FTDI           | ESP32         |
|----------------|---------------|
|*5V from jumper*| 5V            |
| GND            | GND           |
| CTS            |               |
| VCC            |               |
| TX             | UOR           |
| RX             | UOT           |
| DTR            |               |
|----------------|---------------|
||IO0 <-> GND<br> **while programming** |

![Modified from randomnerdtutorials.com][ESP32-CAM-wiring-FTDI1.png]

To use micropython with the webcam, you have to install a version of it
with webcam enabled.

https://github.com/Lennyz1988/micropython/releases has the binary.

If you have set up the esp environment (note that the port will be different than
for the ESP32 Devkit V1):
```
conda activate esp
export AMPY_PORT=/dev/cu.usbserial-A5XK3RJT
```
Connect IO0 to ground and press reset.  Wait 10-15 seconds
```
esptool.py --chip esp32 --port $AMPY_PORT erase_flash
```
Keep the IO0<->ground connection, reset again, wait 10-15 seconds again
```
esptool.py --chip esp32 --port $AMPY_PORT write_flash -z 0x1000 /where/you/download/stuff/firmware.bin
```

(The erase_flash is for when you have been doing something other than micropython.)

Disconnect IO0<->ground.
```
screen $AMPY_PORT 115200
```
and hit reboot.  You should get a prompt.
Play around to determine that python is properly installed.
Then get out of screen (ctrl-A ctrl-\\).

Then upload the relevant files
```
ampy put cred.txt
ampy put connect.py
ampy put main.py
```

Run screen again, reboot, and verify that network connects.  Then within screen :
```
import upip
upip.install('picoweb')
upip.install('micropython-ulogging')
```

You may as well install webrepl now.
```
import webrepl_setup
```
After that has completed rebooting, try out webrepl by connecting,
then downloading webcam.py from
https://github.com/tsaarni/esp32-micropython-webcam
and send it to the esp32.  You should then do:
```
import webcam
webcam.run()
```

At that point, you can go to your browser and connect to the webcam server:
http://192.168.1.114/?flash=true
(replacing the 192.168.1.114 with whatever IP address is in use.)






