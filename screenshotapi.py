from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import timeout_decorator
from PIL import Image

class ScreenshotTimeout(Exception):
    pass

class ScreenshotAPI:
    def __init__(self):
        print("Starting ScreenshotAPI")
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting ScreenshotAPI")
    @timeout_decorator.timeout(20, timeout_exception=ScreenshotTimeout)
    def takescreenshot(self, url, folderpath, filename):
        # instantiate a chrome options object so you can set the size and headless preference
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1800x1200")
        
        # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
        # current directory
        chrome_driver = "chromedriver"
        
        # go to Google and click the I'm Feeling Lucky button
        print("Starting Chrome session...")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

        print("Taking screenshot from: " + url)
        
        self.driver.get(url)

        time.sleep(5)

        # capture the screen
        print("Taking screenshot...")
        self.driver.get_screenshot_as_file(folderpath + "png/" + filename + ".png")
        print("Saved screenshot as: " + folderpath + "png/" +  filename + ".png")

        print("Converting to .jpg...")
        img = Image.open(folderpath + "png/" + filename + ".png")
        basewidth = 600
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        rgb_im = img.convert('RGB')
        rgb_im.save(folderpath + "jpg/" + filename + '.jpg', quality=95)
        print("Converted to: " + folderpath + "jpg/" + filename + ".jpg")
        print("Closing Chrome session...")
        self.driver.quit()

def test():
    with ScreenshotAPI() as scapi:
        scapi.takescreenshot("http://codeformuenster.org/civic-hacking-101/#/", "", "civic-hacking-101.png")

# test()