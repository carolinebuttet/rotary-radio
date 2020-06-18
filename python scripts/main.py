# This script is meant to be used with the instructions found here :
# https://create.arduino.cc/projecthub/carolinebuttet/rotary-musical-phone-14fd79
# This script detects and reads the following phone's inputs:
# - The numbers that are dialed in
# - If the headset is picked up or put down

import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import time
import math
import serial
from pynput.keyboard import Key, Controller

# serial from arduino
# Make sure this number (in my case, 9600) matches the baud rate in your arduino
# Also uptade '/dev/ttyACM0' (the port to which your arduino is connected to the Raspberry Pi) to match your own
# To find your own port, type ' ls /dev/tty* ' in the raspberry Pi's terminal and you will find all your available ports.
# Your arduino will be listed there.
# Comment this line if you don't have an arduino connected to the raspberry pi, otherwise the script will not work.
ser = serial.Serial('/dev/ttyACM0', 9600)

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

# Set pin 10, 16 and 18 to be an input pin and set initial value to be pulled low (off)
# Pin 18 is connected to the pick up / put down switch
# Pin 16 is connected to the rotary module (to the switch that opens / closes when the dial started / ended)
# Pin 10 is connected to the rotary module (to the switch that opens / closes when the rotary module is released)
# For example, pin 10 will be open and closed 7 times if number 7 is dialed.
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# set the led pin for blinking (physical pin number 15)
ledpin = 15
# the number of seconds that the LED will stay on / off
blinktimer = 1
# start the timer
start = time.time()
# a boolean to control the LED's state
led_is_on = False

# Set the ledpin to be an output
GPIO.setup(ledpin, GPIO.OUT)

increment = 0
# get the input for the start of the dial
old_num_state = GPIO.input(16)
num_state = GPIO.input(16)

# get thte input for the pick up / down switch
old_dial_state = GPIO.input(10)
dial_state = GPIO.input(10)

# get the input for the dialed numbers
old_pick_up_state = GPIO.input(18)
pick_up_state = GPIO.input(18)

# some global variables that will be used
global dial_count
dial_count = 0
global date
date = 0
global is_picked_up
is_picked_up = False
global keyboard

# The keyboard controller, that allows this script to send keyboard signals.
keyboard = Controller()

country_state = True
old_country_state = True


# This function registers the dialed date.
def register_date(year):
    global keyboard
    print("Register date", year)
    # refresh the page if the dialed date is 1111 (with the shortcul CTRL + R)
    if year == 1111:
        print("reload page")
        keyboard.press(Key.ctrl)
        keyboard.press('r')
        keyboard.release(Key.ctrl)
        keyboard.release('r')
    # we round the year to the nearest 10 (1962 becomes 1960)
    rounded_year = round(year, -1)
    print(rounded_year)
    # we then emulate the corresponding keypress
    # that keypress will then be interpreted by our chrome extension
    # and perform the corresponding changes to our webpage.
    if rounded_year == 1900:
        keyboard.press('0')
        keyboard.release('0')
    if rounded_year == 1910:
        keyboard.press('1')
        keyboard.release('1')
    if rounded_year == 1920:
        keyboard.press('2')
        keyboard.release('2')
    if rounded_year == 1930:
        keyboard.press('3')
        keyboard.release('3')
    if rounded_year == 1940:
        keyboard.press('4')
        keyboard.release('4')
    if rounded_year == 1950:
        keyboard.press('5')
        keyboard.release('5')
    if rounded_year == 1960:
        keyboard.press('6')
        keyboard.release('6')
    if rounded_year == 1970:
        keyboard.press('7')
        keyboard.release('7')
    if rounded_year == 1980:
        keyboard.press('8')
        keyboard.release('8')
    if rounded_year == 1990:
        keyboard.press('9')
        keyboard.release('9')
    if rounded_year == 2000:
        keyboard.press('q')
        keyboard.release('q')
    if rounded_year == 2010:
        keyboard.press('w')
        keyboard.release('w')
    if rounded_year == 2020:
        keyboard.press('e')
        keyboard.release('e')


# This function registers the dialed number
# And turns the dialed number into a usable date
# So that the numbers 1-9-6-0 can be interpreted as the number 1960
def register_number(num):
    global dial_count
    global date
    # if the switch has detected 10 open / closed signals, then this means that the number dialed is 0.
    if num == 10:
        num = 0
    # if this is the first number of our date that is dialed, multiply it by 1000
    if dial_count == 1:
        date += num * 1000

    # if this is the second number of our date that is dialed, multiply it by 100
    if dial_count == 2:
        date += num*100

    # if this is the third number of our date that is dialed, multiply it by 10
    if dial_count == 3:
        date += num*10

    # if this is the fourth number of our date that is dialed, we don't do anything
    if dial_count == 4:
        date += num
        dial_count = 0
        print(date)
        # we register the date if we have 4 numbers dialed (like 1-9-6-0)
        register_date(date)
        date = 0
    print(date)


# The main loop
while True:  # Run forever

    # blink stuff
    remaining = blinktimer + start - time.time()
    if remaining > 0:
        if led_is_on == False:
            GPIO.output(ledpin, GPIO.HIGH)
            led_is_on = True
    if remaining <= 0:
        if led_is_on == True:
            GPIO.output(ledpin, GPIO.LOW)
            led_is_on = False
        if remaining <= blinktimer*-1:
            start = time.time()

    # phone stuff
    pick_up_state = GPIO.input(18)
    num_state = GPIO.input(16)
    dial_state = GPIO.input(10)

    # check the handset state
    if pick_up_state != old_pick_up_state:
        if pick_up_state == 1:
            # the handset is picked up, let's play the music
            print("pick up")
            is_picked_up = True
            # we press the space bar (that plays and pause the music on the website)
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        else:
            print("pick down")
            # the handset is put down, let's pause the music
            is_picked_up = False
            date = 0
            dial_count = 0
            # we press the space bar (that plays and pause the music on the website)
            keyboard.press(Key.space)
            keyboard.release(Key.space)

    # if the phone is picked up
    # we listen for the dialed numbers
    if is_picked_up:
        if num_state != old_num_state:
            if num_state == 1:
                increment = increment + 1
        old_num_state = num_state

        if dial_state != old_dial_state:
            if dial_state == 1:  # dialing started
                print("dial started")
                increment = 0
            if dial_state == 0:
                dial_count = dial_count+1
                print("dial ended")
                # the dialing ended, we can register the number
                register_number(increment+1)
                # if we have dialed 4 numbers, (for example 1-9-6-0)
                # we can register the date and reset the dial count
                # and reset the dial_count value
                if dial_count == 4:
                    dial_count = 0

    # serial stuff
    # here we check for the arduino's signal
    # and we press the corresponding keys if needed
    # Comment this section if you don't have an arduino connected to the raspberry pi, otherwise the script will not work.
    if(ser.in_waiting > 0):  # if we have someting
        line = ser.readline().decode('utf-8')  # we read and decode the line
        # we only get the first 2 characters of this line
        country_code = line[0:2]
        # and we emulate the corresponding key presses for each country code
        if country_code == "US":  # USA
            keyboard.press('r')
            keyboard.release('r')
        if country_code == "CL":  # COLOMBIA
            keyboard.press('t')
            keyboard.release('t')
        if country_code == "UK":  # United Kingdom
            keyboard.press('z')
            keyboard.release('z')
        if country_code == "FR":  # France
            keyboard.press('u')
            keyboard.release('u')
        if country_code == "TU":  # Turkey
            keyboard.press('i')
            keyboard.release('i')
        if country_code == "ML":  # Mali
            keyboard.press('o')
            keyboard.release('o')
        if country_code == "MD":  # Madagascam
            keyboard.press('p')
            keyboard.release('p')
        if country_code == "RU":  # Russia
            keyboard.press('a')
            keyboard.release('a')
        if country_code == "JP":  # Japan
            keyboard.press('s')
            keyboard.release('s')
        if country_code == "NZ":  # New Zealand
            keyboard.press('d')
            keyboard.release('d')

    # Reset the values between each loop
    old_dial_state = dial_state
    old_pick_up_state = pick_up_state
    old_country_state = country_state
    # Add delay for stability
    time.sleep(0.01)
