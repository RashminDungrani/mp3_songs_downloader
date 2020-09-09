"""
Author: Rashmin Dungrani
Date:   21-Jan-2020
Discription:    This Python Script can Download song from mp3paw website and Downloaded mp3 file is Store in /home/{username}/Music Directory
"""


from sys import argv
from time import sleep
from os import system as os_system
import traceback

download_path = "/home/jarvis/Music/"

browser = None

def strat_browser():
    from selenium import webdriver

    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", download_path)
    profile.set_preference("browser.download.useDownloadDir", True)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/mpeg")
    global browser
    browser = webdriver.Firefox(profile,firefox_options=options)
    
def song_downlaoder(songName):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC

    strat_browser()
    os_system('clear')
    # print("Press 0 to Exit")
    # songName = input("Song Name : ")
    # if songName == "0":
    #     for handle in browser.window_handles:
    #         browser.switch_to.window(handle)
    #         browser.close()
    #     exit()

    print("\nSearching...\n")
    browser.get("https://mp3paw.com/")
    searchField = browser.find_element_by_id("search")
    searchField.send_keys(songName)
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'submit')))
    browser.find_element_by_id("submit").click()

    firstFiveSongsName = []
    print("\n\t\t***** Select Your Song ******\n")
    print("No. Duration    Song Name\t\t\t\t\tCount")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/div[1]/div[1]/h3")))
    for song_num in range(1,6):
        duration = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div["+str(song_num)+"]/div[1]/span")
        name = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div["+str(song_num)+"]/div[1]/h3")
        listenCount = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div["+str(song_num)+"]/div[2]/span[2]/span[2]")
        name = name.text
        songName = name[0:41] + "..." if len(name) > 44 else name + " "*(44-len(name))
        print(" "+str(song_num)+"\t"+duration.text+"\t" + songName + "\t" + listenCount.text)
        firstFiveSongsName.append(name)

    print("\nPress 0 if your song is not listed below")
    while True:
        try:
            song_number = int(input("Choose Song Number : "))
            if not song_number:
                browser.close()
                return
            if song_number in range(1, 6):
                break
            else:
                print('😡 choose from 1 to 5')
        except ValueError:
            print('😡 only integer valid')

    songName = str(firstFiveSongsName[int(song_number)-1])
    print("\nDownloading " + songName)
    # Click To Download Button
    sleep(0.2)
    browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div['+str(song_number)+']/div[3]/ul/li[3]/div').click()
    handles = browser.window_handles
    browser.switch_to.window(handles[1])
    WebDriverWait(browser, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[3]/ul/li[4]')))
    sleep(0.2)
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div[3]/ul/li[4]').click()

    mp3_file_name = download_path + songName + '.mp3'
    from os.path import exists
    # check download start
    print(mp3_file_name + '.part from check download start')
    while not exists(mp3_file_name + '.part'):
        sleep(1)

    print('\n\tDownloading Started... Wait')
    sleep(1)
    handles = browser.window_handles
    browser.switch_to.window(handles[2])
    browser.close()
    browser.switch_to.window(handles[1])
    browser.close()
    browser.switch_to.window(handles[0])
    browser.get('about:blank')
    # wait for file Downloaded
    while exists(mp3_file_name + '.part'):
        sleep(1)
    if exists(mp3_file_name):
        print('Download Completed')
    else:
        print('Something wrong')
    browser.close()
    return True

try:
    songName = ' '.join(argv[1:])
    if len(argv) > 1:
        # TODO: if song name matched found in Music then Show and ask for play in vlc
        song_downlaoder(songName)
    else:
        print('Write song name after script name')
except KeyboardInterrupt:
    for handle in browser.window_handles:
        browser.switch_to.window(handle)
        browser.close()
    print('terminated')

except Exception as e:
    print(e)
    print("\n\n*********** ERROR ***********\n")
    traceback.print_exc()
