# BruteForcePlexPin
Brute force plex pin experiment


_____________________________________________________


Experiment to test the security of Plex server and how easy/hard it would be to brute force the admin users pincode.

The conclusion was that there must be some sort of hidden brute force defense mechanism in the pin login system. After an unknown number of failed attempts, the correct pin has the same effect as the wrong pin.


BRUTE FORCE PLEX PIN V2 (BFPPv2.py) Using selenium web browser and python to bruteforce the plex server home users pin code.!

Requirements:

    Install python3 and use pip to install libraries needed.
    Pip should be installed automatically with python3 : https://www.python.org/downloads/

    Commands to run:
        >> pip install -r requirements.txt
        >> python BFPPv2.py

    Also make sure you have the latest chromedriver, found here https://chromedriver.chromium.org/downloads
    Place the exe in the same folder as 'BFPPv2.py'
    Also make sure your chrome browser is up to date: chrome://settings/safetyCheck -> check now (update)

Usage:

    Launch the program!
    Login to your Plex server home user..
    Select the user you want to bruteforce..
    The program will begin..
	Watch the command promt to determin: current pin, pins/keys per second (K/s), Estimated time of arrival (ETA)
