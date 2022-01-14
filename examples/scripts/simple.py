import time

def run(browser):
    while True:
        browser.get('https://twitter.com/explore/tabs/trending')

        # reload hourly
        time.sleep(60*60)

