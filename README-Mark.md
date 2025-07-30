# PI setup

We want micropython

The upstream repo is:

https://www.waveshare.com/wiki/Pico-Clock-Green




sudo zypper install cross-arm-none-newlib-devel cross-arm-binutils cross-arm-none-gcc14-bootstrap

# Micropython


https://github.com/domneedham/pico-clock-green-python?tab=readme-ov-file


We need the firmware from:

https://projects.raspberrypi.org/en/projects/get-started-pico-w/2


To install, drop into the mass storage device

To get shell:

mpremote


>>> import mip
>>>
>>> mip.install('umqtt.simple')
Installing umqtt.simple (latest) from https://micropython.org/pi/v2 to /lib
Copying: /lib/ssl.mpy
Copying: /lib/umqtt/simple.mpy
Done



