import time

def run(browser):
    while True:
        browser.get('https://www.bing.com/')
        time.sleep(60*60)

