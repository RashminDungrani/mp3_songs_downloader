"""
Author: Rashmin Dungrani
Date:   21-Jan-2020
Discription:    This Python Script can Download song from mp3paw website and Downloaded mp3 file is Store in /home/{username}/Music Directory
"""


from selenium import webdriver
from time import sleep
import os
import sys
import traceback


def song_downlaoder():
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", "/home/jarvis/Music") # Change download location
    profile.set_preference("browser.download.useDownloadDir", True)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/mpeg")
    driver = webdriver.Firefox(profile,firefox_options=options)

    while 1:
        os.system('clear')
        print("Press 0 to Exit")
        songName = input("Song Name : ")
        if songName == "0":
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                driver.close()
            exit()

        print("\nSearching...\n")
        link = "https://mp3paw.com/"
        driver.get(link)
        searchField = driver.find_element_by_id("search")
        searchField.send_keys(songName)
        sleep(0.1)
        driver.find_element_by_id("submit").click()
        sleep(0.8)

        firstFiveSongsName = []
        print("\n\t\t***** Select Your Song ******\n")
        print("No. Duration    Song Name\t\t\t\t\tCount")
        for song_num in range(1,6):
            duration = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div["+str(song_num)+"]/div[1]/span")
            name = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div["+str(song_num)+"]/div[1]/h3")
            listenCount = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div["+str(song_num)+"]/div[2]/span[2]/span[2]")
            name = name.text
            songName = name[0:41] + "..." if len(name) > 44 else name + " "*(44-len(name))
            print(" "+str(song_num)+"\t"+duration.text+"\t" + songName + "\t" + listenCount.text)

            firstFiveSongsName.append(name)

        print("\nPress 0 if your song is not listed below")
        song_number = input("Choose Song Number : ")
        while 1:
            if int(song_number) in range(1,6):
                print("Downloading " + str(firstFiveSongsName[int(song_number)-1]))
                # Click To Download Button
                driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div['+str(song_number)+']/div[3]/ul/li[3]/div').click()
                sleep(2)
                handles = driver.window_handles
                driver.switch_to.window(handles[1])
                sleep(1)
                driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/ul/li[4]').click()
                print('\n\tDownloading Started... Wait')
                sleep(6)
                print('\n\tSong Downloaded')
                break
            elif song_number == "0":
                break
            else:
                print("Invalid input Try Again...")

try:
    song_downlaoder()
except Exception as e:
    print(e)
    print("\n\n*********** ERROR ***********\n")
    traceback.print_exc()
