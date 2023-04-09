#!/usr/bin/env python3

# Main controller for my InkyPi project.
# Main loop will wait for user user inputs/ timer events and then execute appropriate code.

import os
import json
import signal
import logging
import RPi.GPIO as GPIO

import quote
import syncnotes
import displayControler

library = quote.BookList()
library.load()
library = syncnotes.syncQuotes(library, loadSettings())
library.save()


# Shutdown the device 
def Shutdown():  
    os.system("sudo shutdown -h now")  

def loadSettings():
    # get settings from JSON file
    with open("settings.json") as json_file:
        data = json.load(json_file)

        settings["profile"] = data["profile"]
        settings["colorsToSync"] = data["colorsToSync"]

    # get credentials for JSON file
    with open("credentials.json") as json_file:
        data = json.load(json_file)

        # get email and password from settings
        settings["email"] = data["email"]
        settings["password"] = data["password"]
    return settings




# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = ['A', 'B', 'C', 'D']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    q = library.randomQuote()
    displayControler.displayQuote(q[0],q[1])
    print("Button press detected on pin: {pin}")


# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
signal.pause()




# FOR TESTING sync quotes
# library = syncnotes.syncQuotes(library, loadSettings())
# library.save()

# FOR TESTING random quote
# l = library.randomQuote()
# print(l[0].text, l[1].title, l[1].author)

# FOR TESTING display a random quote
# q = library.randomQuote()
# displayControler.displayQuote(q[0],q[1])

# FOR TESTING find a specific quote
# b = [book for book in library.books if book.title == "A Compact Guide to the Whole Bible"]
# q = [quote for quote in b[0].quotes if quote.text == "A third quality of God is God\u2019s power, but this quality can be both positive and negative. God\u2019s power to create, to rescue, and to punish the wicked is seen as a positive thing, but God\u2019s power is also frightening, particularly when it is directed against humans (cf. Job 9:1\u201319)."]
# displayControler.displayQuote(q[0],b[0])