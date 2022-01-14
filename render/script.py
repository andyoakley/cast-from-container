import time
import logging

def run(browser):
    while True:
        browser.get('https://www.bing.com')
        time.sleep(120)

logging.warning("Using default script. You probably want to mount something to /app/script.py instead.")