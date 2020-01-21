"""
Author: Rashmin Dungrani
Date:   21-Jan-2020
Python 3
Discription:    This Python Script will Download song from mp3paw website and Downloaded mp3 file is 128kbps
"""


from selenium import webdriver
from time import sleep
import os


def song_downlaoder(songName):
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2);
    profile.set_preference("browser.download.dir", "/home/jarvis/Music"); # Change download location
    profile.set_preference("browser.download.useDownloadDir", True);
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/mpeg");

    # songName = input("Enter Song Name : ")
    print("Hold on...")
    driver = webdriver.Firefox(profile,firefox_options=options)
    link = "https://mp3paw.com/"
    driver.get(link)
    searchField = driver.find_element_by_id("search")
    searchField.send_keys(songName)
    sleep(1)
    driver.find_element_by_id("submit").click()
    sleep(2)
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div[3]/ul/li[3]/div').click()
    sleep(2)
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    sleep(1)
    print('Downloading...')
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/ul/li[4]').click()
    driver.close()

try:
    songName = input("Song Name : ")
    song_downlaoder(songName)
except Exception as e:
    print(e)
