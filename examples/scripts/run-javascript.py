import time

def coinmarketcap_heatmap(browser):
        browser.get('https://coinmarketcap.com/crypto-heatmap/')
        browser.execute_script("""
        var el = document.getElementsByClassName('treeWrap')[0];
        el.style.position = 'fixed';
        el.style.top = 0;
        el.style.left = 0;
        el.style.zIndex = 999;
        """)

def coinmarketcap_dark(browser):
    browser.get('https://coinmarketcap.com/')
    browser.execute_script("""
    var el = document.getElementsByClassName('icon-Moon')[0];
    el.click();
    """)


def run(browser):
    coinmarketcap_dark(browser)
    time.sleep(60)

    while True:
        coinmarketcap_heatmap(browser)
        time.sleep(60)
