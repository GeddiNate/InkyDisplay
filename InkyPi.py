#!/usr/bin/env python3

# Main controller for my InkyPi project.
# Main loop will wait for user user inputs/ timer events and then execute appropriate code.

import os
import json
import signal
import logging
#import RPi.GPIO as GPIO
from enum import Enum

import quote
import syncnotes


# Enum for different modes
class Mode(Enum):
    KINDLE = 1
    SPOTIFY = 2


# Shutdown the device 
def Shutdown():  
    os.system("sudo shutdown -h now")  

# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    
    # if bottom button pressed
    if pin == BUTTONS[3]:
        # change current mode to SPOTIFY
        if currentMode == Mode.KINDLE:
            currentMode = Mode.SPOTIFY
        # change current mode to KINDLE
        elif currentMode == Mode.SPOTIFY:
            currentMode = Mode.KINDLE

    # if displaying kindle highlights
    elif currentMode == Mode.KINDLE:
        # if top button pressed
        if pin == BUTTONS[0]:
            nextQuote()
        # if top mid button pressed
        elif pin == BUTTONS[1]:
            prevQuote()
        # if low min button pressed
        elif pin == BUTTONS[2]:
            changeBackground()

    # if displaying current spotify track  
    elif currentMode == Mode.SPOTIFY:
         # if top button pressed
        if pin == BUTTONS[0]:
            nextTrack()
        # if top mid button pressed
        elif pin == BUTTONS[1]:
            prevTrack()
        # if low min button pressed
        elif pin == BUTTONS[2]:
            pause()



        



# currentMode = Mode.KINDLE
# # GPIO pins for each button (from top to bottom)
# BUTTONS = [5, 6, 16, 24]

# # Set up RPi.GPIO with the "BCM" numbering scheme
# GPIO.setmode(GPIO.BCM)

# # Buttons connect to ground when pressed, so we should set them up
# # with a "PULL UP", which weakly pulls the input signal to 3.3V.
# GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)



    



# # Loop through out buttons and attach the "handle_button" function to each
# # We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# # picking a generous bouncetime of 250ms to smooth out button presses.
# for pin in BUTTONS:
#     GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

# # Finally, since button handlers don't require a "while True" loop,
# # we pause the script to prevent it exiting immediately.
# signal.pause()







# # # main loop 
# # def main():



# # if __name__ == '__main__':
# #     main()


# try to open saved quotes
try:
    f = open("output.json")
# if file not found create empty array to store data
except FileNotFoundError:
    books = []
# if unknown exception
except Exception as e:
    logging.exception(e)
    books = []
# if file found load data from file
else:
    books = quote.loadQuotes(f)
# close file
f.close()


settings = {"profile": "C:\\Users\\natha\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1"}

with open("credentials.json") as json_file:
    data = json.load(json_file)

    # get email and password from settings
    settings["email"] = data["email"]
    settings["password"] = data["password"]
    


syncnotes.syncQuotes(books, settings)