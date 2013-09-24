#!/usr/bin/python
import time
import array
import argparse
from subprocess import call
# this is a test script for sending on/off commands to
# Belkin BG108000-04 Conserve Energy-Saving Surge Strip
# using the RF transmitters found at https://www.sparkfun.com/products/10534
# and the raspberry Pi GPIO pins

parser = argparse.ArgumentParser(description='determine on/off command')
parser.add_argument('--pwr', dest='cmdItem', default='off')

args = parser.parse_args()

#setting up our pin(s), and the pin-out numbering scheme to use
# commands are an array of on/off signals
# a detailed overview of how to grab this information is available
# at http://rayshobby.net/?p=2427
# also...some dismantling was required of the transmitter as there is
# a small spst switch that lets you set 3 of the pins high or low
# and thus changes your on/off commands

cmdON = [0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1,1,0,0,0,1,0]
cmdOFF = [0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,1,1,0,0,1,1,1,0,0]

#functions to open the gpio "value" file and write
#the on/off values. The RF transmitters are not currently too
#timing sensitive, so this has been working

def writeOn():
    f = open('/sys/class/gpio/gpio17_pg9/value', 'w+')
    f.write('1')
    f.close()

def writeOff():
    f = open('/sys/class/gpio/gpio17_pg9/value', 'w+')
    f.write('0')
    f.close() 

def sendRF(cmd):
    for click in range(0,16):
        for blip in range(0,25):
            if cmd[blip] == 1:
                writeOn() 
                time.sleep(0.000480)
                writeOff()
                time.sleep(0.000160)
            else:
                writeOn() 
                time.sleep(0.000160)
                writeOff() 
                time.sleep(0.000480)
        time.sleep(0.005)

if args.cmdItem == 'on':
    sendRF(cmdON)

if args.cmdItem == 'off':
    sendRF(cmdOFF)

