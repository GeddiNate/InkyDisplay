#!/usr/bin/env python3
import subprocess


# Main controller for my InkyPi project.
# Main loop will wait for user user inputs/ timer events and then execute appropriate code.

import os
import json
import signal
import logging
import RPi.GPIO as GPIO

import highlight
import synchighlights
import displayControler
import subprocess


def getHighlightFile():
    # Set the source and destination paths
    with open("credentials.json") as f:
        paths = json.load(f)
        source_path = paths["data_location"]
        destination_path = paths["pi_storage"]

        # Define the command to execute
        command = ['scp', source_path, destination_path]

        # Execute the command and capture the output
        output = subprocess.check_output(command)
        logging.log(output)
        print(output)


# Shutdown the device 
def Shutdown():  
    os.system("sudo shutdown -h now")  



# library = highlight.BookList()
# library.load()

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
    q = library.randomHighlight()
    displayControler.displayHighlight(q[0],q[1])
    print("Button press detected on pin: {pin}")


# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
signal.pause()




# FOR TESTING sync highlights
# library = syncnotes.syncHighlights(library, loadSettings())
# library.save()

# FOR TESTING random highlight
# l = library.randomHighlight()
# print(l[0].text, l[1].title, l[1].author)

# FOR TESTING display a random highlight
# q = library.randomHighlight()
# displayControler.displayHighlight(q[0],q[1])

# FOR TESTING find a specific highlight
# b = [book for book in library.books if book.title == "A Compact Guide to the Whole Bible"]
# q = [highlight for highlight in b[0].highlights if highlight.text == "A third quality of God is God\u2019s power, but this quality can be both positive and negative. God\u2019s power to create, to rescue, and to punish the wicked is seen as a positive thing, but God\u2019s power is also frightening, particularly when it is directed against humans (cf. Job 9:1\u201319)."]
# displayControler.displayHighlight(q[0],b[0])

def main():
    getHighlightFile()
    library = highlight.BookList()
    library.load()
    randHighlight = library.randomHighlight()
    displayControler.displayhighlight(randHighlight[0], randHighlight[1])

if __name__ == "__main__":
    main()