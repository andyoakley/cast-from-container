import time
import os
import sys
import logging
logging.basicConfig(level=logging.INFO)
from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import script

def create_driver():
    logging.info("Creating driver")

    op = webdriver.ChromeOptions()
    #op.add_argument("--disable-gpu")
    op.add_argument("--disable-dev-shm-usage")
    op.add_argument('--force-dark-mode')

    browser = webdriver.Chrome(options=op)
    browser.set_window_size(1920, 1200)

    return browser

def wait_for_chromecast(browser, name):
    while True:
        logging.info("Looking for Chromecast {name}")
        s = browser.get_sinks()

        for sink in s:
            if sink['name'] == name:
                return name

        time.sleep(5)

def wait_for_first_chromecast(browser):
    no_sinks_found = 0
    
    while no_sinks_found <= 12:
        logging.info("Looking for first Chromecast")
        s = browser.get_sinks()
        if len(s) > 0:
            name = s[0]['name']
            logging.info(f"Found Chromecast {name}")
            if 'session' in s[0]:
                logging.info(f'Chromecast is busy with \'{s[0]["session"]}\'. Waiting.')
            else:
                return name
        else:
            no_sinks_found += 1

        time.sleep(5)

    if no_sinks_found > 12:
        logging.warning("Couldn't find any Chromcast devices")
        sys.exit(2)


browser = create_driver()
name = wait_for_first_chromecast(browser)

# TODO: Do we want to always seize the session or wait until free?

logging.info(f"Starting mirroring to {name}")
browser.start_tab_mirroring(name)
time.sleep(5)

# this is most of the user-specified navigation
logging.info(f"Start user script")
user_script = Thread(target=lambda: script.run(browser))
user_script.daemon = True  # terminates when main thread terminates
user_script.start()

# main thread will make sure we're still casting
healthy = True

# failure modes:
#  - chromecast missing
#  - chromecast casting someone else
while healthy:
    time.sleep(60)

    sinks = browser.get_sinks()
    healthy = False
    for sink in browser.get_sinks():
        if (sink['name'] == name) and ('session' in sink) and (sink['session'] == 'Casting tab'):
            healthy = True

    if not user_script.is_alive():
        logging.warning("User script seems to have crashed")
        healthy=False


logging.warning('Casting session no longer healthy')
sys.exit(1)

