"""
Michael Patel
April 2019

version: Python 3.6.5

File Description:

Notes:
    - chromedriver.exe (Chrome) is in '\AppData\Local\Programs\Python\Python36\Scripts' directory
    - geckodriver.exe (Firefox) is in '\AppData\Local\Programs\Python\Python36\Scripts' directory
    - SoundCloud API page: https://developers.soundcloud.com/docs/api/guide
    - https://www.google.com/search?client=firefox-b-1-d&q=python+selenium+could+not+be+scrolled+into+view

"""

################################################################################
# IMPORTs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


################################################################################
# Engineers Play SoundCloud url
url = "https://soundcloud.com/engineers-play"

# Engineers Play YouTube channel
url = "https://www.youtube.com/channel/UCOPA21itTLMQqGDDm88wHjg/videos"

chromedriver_path = ""
driver = webdriver.Firefox()
driver.get(url)
print(driver.title)
time.sleep(1)
driver.find_element_by_id("items").click()

#print(element.text)
#driver.close()
