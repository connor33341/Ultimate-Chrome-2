from __future__ import annotations

from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
from time import sleep
from replit import db
from threading import Thread
from uuid import uuid4
#import pyautogui

from localstorage import LocalStorage

# change this to a website like discord.com to enable LocalStorage
SINGLE_PAGE = False#"https://connor33341.github.io/static/virtualkeyboard/iframe/index.html?src=https://wikipedia.org"
STARTING_PAGE = "https://duckduckgo.com"
TARGET_ELEMENT = "q"
KEYS = str(input("Keys: "))

def is_cookies() -> None:
    return len([key for key in db.keys() if key.isnumeric()]) > 0


def assemble_url(cookie: dict) -> str:
    url = ""

    url += "https://" if cookie["secure"] else "http://"

    url += cookie["domain"].lstrip(".")
    url += cookie["path"]

    return url


def save_cookies(driver: Chrome) -> None:
    print("Saving cookies...", end="")
    try:
        for key in [key for key in db.keys() if key.isnumeric()]:
            del db[key]
        for index, value in enumerate(driver.get_cookies()):
            db[str(index)] = value
    except Exception:
        print("fail")
    else:
        print("done")


def load_cookies(driver: Chrome) -> None:
    print("Loading cookies...", end="")
    try:
        for key in sorted([key for key in db.keys() if key.isnumeric()],
                          key=lambda key: int(key)):
            cookie: dict = db[key]
            # url = assemble_url(cookie)
            # if urlparse(driver.current_url).hostname != urlparse(url).hostname:
            #     driver.get(url)
            driver.add_cookie(dict(cookie))
    except Exception:
        print("fail")
    else:
        print("done")


def is_localstorage() -> None:
    return len([key for key in db.keys() if key.isalpha()]) > 0


def save_localstorage(ls: LocalStorage) -> None:
    print("Saving LocalStorage...", end="")
    try:
        for key, value in ls.items():
            db[key] = value
    except Exception:
        print("fail")
    else:
        print("done")


def load_localstorage(ls: LocalStorage) -> None:
    print("Loading LocalStorage...", end="")
    assert SINGLE_PAGE
    try:
        for key, value in [key for key in db.keys() if key.isalpha()]:
            ls[key] = value
    except Exception:
        print("fail")
    else:
        print("done")

def rec():
    while True:
        ID = str(uuid4())
        Url = driver.current_url
        Url.removeprefix("https://")
        Url.replace("/","-")
        Url.replace(".","-")
        #driver.save_screenshot(f"rec/{ID}.png")
if __name__ == "__main__":
    print("Starting Ultimate Chrome 2...")

    chrome_options = ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # kiosk
    if SINGLE_PAGE:
        chrome_options.add_argument('--kiosk')
    else:
        chrome_options.add_argument("start-maximized")

    driver = Chrome(options=chrome_options)
    ls = LocalStorage(driver)

    if SINGLE_PAGE:
        driver.get(SINGLE_PAGE)

    if is_cookies():
        print("Found some cookies to restore!")
        load_cookies(driver)

    if SINGLE_PAGE and is_localstorage():
        print("Found some LocalStorage data to restore!")
        load_localstorage(ls)

    if not SINGLE_PAGE:
        #old: "https://uc-2-landing-regulad.replit.app/"
        driver.get(STARTING_PAGE)
        SearchBox = driver.find_element(By.NAME, TARGET_ELEMENT)
        SearchBox.send_keys(KEYS+Keys.RETURN)
    
    print("Done loading! Stop the repl to save cookies.")

    try:
        RecThread = Thread(target=rec)
        RecThread.start()
        Running = True
        while Running:
            sleep(0.1)
            #save_cookies(driver)
            try:
                Command = input("Text: ")
                if Command == "<ENTER>":
                    Command = Keys.RETURN
                if Command == "<TAB>":
                    Command = Keys.TAB
                if Command == "<CTRL>":
                    Command = Keys.CONTROL
                if Command == "<SHIFT>":
                    Command = Keys.SHIFT
                if Command == "<ESC>":
                    Command = Keys.ESCAPE
                if Command == "<BACKSPACE>":
                    Command = Keys.BACKSPACE
                if Command == "<DEL>":
                    Command = Keys.BACKSPACE
                if Command == "<END>":
                    Running = False
                    break
                AC = ActionChains(driver)
                AC.send_keys(Command)
                AC.perform()
                #pyautogui.click()
                #pyautogui.typewrite(Command)
            except Exception as Error:
                print(Error)
            if SINGLE_PAGE:
                save_localstorage(ls)
    except KeyboardInterrupt:
        print("Recieved an interrupt! Shutting down...")
    finally:
        save_cookies(driver)
        driver.close()
