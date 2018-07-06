#!/usr/bin/env python

#####################################################################################
# This script will allow you to use an Amazon Dash Button to toggle two functions.  #
# In this case, it toggles two PiMote sockets by Energenie, but the functions can   #
# be anything you like!                                                             #
#                                                                                   #
# By Wesley Archer (AKA. @raspberrycoulis)                                          #
# https://raspberrycoulis.com | https://github.com/raspberrycoulis                  #
#                                                                                   #
# Special thanks to OyaMist Aeroponics on Raspberry Pi Stack Exchange for their     #
# assistance with this --> https://github.com/oyamist                               #
#####################################################################################

# Import the required modules
import RPi.GPIO as GPIO
import time
import requests
import logging
import urllib
import httplib
import os
import threading

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

# Set your Dash Button's MAC address below - must be lowercase.
DASH_BUTTON_MAC = 'xx:xx:xx:xx:xx:xx'

# Prevent GPIO warnings
GPIO.setwarnings(False)

# Function to turn on both PiMote sockets
def both_on():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.output (22, False)
    GPIO.output (18, False)
    GPIO.output (11, False)
    GPIO.output (15, False)
    GPIO.output (16, False)
    GPIO.output (13, False)
    GPIO.output (11, True)
    GPIO.output (15, True)
    GPIO.output (16, False)
    GPIO.output (13, True)
    time.sleep(0.1)
    GPIO.output (22, True)
    time.sleep(0.25)
    GPIO.output (22, False)
    GPIO.cleanup()

# Function to turn off both PiMote sockets
def both_off():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.output (22, False)
    GPIO.output (18, False)
    GPIO.output (11, False)
    GPIO.output (15, False)
    GPIO.output (16, False)
    GPIO.output (13, False)
    GPIO.output (11, True)
    GPIO.output (15, True)
    GPIO.output (16, False)
    GPIO.output (13, False)
    time.sleep(0.1)
    GPIO.output (22, True)
    time.sleep(0.25)
    GPIO.output (22, False)
    GPIO.cleanup()

# Function that sets the lackClick variable when the Dash Button is pushed
def button_pressed_dash():
    global lastClick
    lastClick = time.time()

# This function sets and handles the states set by the button pushes
def state_machine():
    STATE1 = 1
    STATE2 = 2
    INITIAL_STATE = STATE1
    DEBOUNCE_SECONDS = 1
    state = INITIAL_STATE
    global lastClick
    lastClick = 0 # wait for next button click
    while True:
        elapsed = time.time() - lastClick
        ###### state definitions and transitions
        if state == STATE1:  # STATE1 actions and transitions
           if lastClick != 0 and elapsed > DEBOUNCE_SECONDS:
               both_on()        # Change this function if you want to!
               lastClick = 0    # we handled click
               state = STATE2   # goto STATE2
        elif state == STATE2:   # STATE2 actions and transitions
           if lastClick != 0 and elapsed > DEBOUNCE_SECONDS:
               both_off()       # Change this function if you want to!
               lastClick = 0    # we handled click
               state = INITIAL_STATE
        time.sleep(0.1)

# This is required to get the UDP packet sent by the Dash Button when pushed.
def udp_filter(pkt):
    options = pkt[DHCP].options
    for option in options:
        if isinstance(option, tuple):
            if 'requested_addr' in option:
                mac_to_action[pkt.src]()
                break

# Below is required to ensure the Dash Button is detected when pushed.
mac_to_action = {DASH_BUTTON_MAC : button_pressed_dash} # Add your Amazon Dash Button's MAC address in lowercase
mac_id_list = list(mac_to_action.keys())
# create separate thread for state machine
stateMachineThread = threading.Timer(0.1, state_machine)
stateMachineThread.daemon = True
stateMachineThread.start()
sniff(prn=udp_filter, store=0, filter="udp", lfilter=lambda d: d.src in mac_id_list)
