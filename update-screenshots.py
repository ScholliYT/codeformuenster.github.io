import json
from screenshotapi import ScreenshotAPI
from screenshotapi import ScreenshotTimeout
import sys

print("Reading repo json file...")
with open('json/repos.json') as f:
    repodata = json.load(f)


with ScreenshotAPI() as scapi:
  for repo in repodata:
    
    reponame = repo["name"]
    html_url = repo["html_url"]
    if(html_url):
      print("\n")
      try:
        scapi.takescreenshot(html_url, "screenshots/fromPython/", reponame)
      except ScreenshotTimeout:
        print("!=> Timed out while taking screenshot!")
      except:
        print("!=> Error taking screenshot!")
      print("\n")
    else:
      print("!=> No URL For: " + reponame)