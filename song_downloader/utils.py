import os
import json
import readline
from platform import system
from song_downloader.locations import Paths


def check_download_path_available() -> bool:
    if not os.path.exists(Paths.config_path):
        with open(Paths.config_path, 'w') as config_file:
            json.dump({"download_path": ""}, config_file, indent=4, ensure_ascii=False) 

    with open(Paths.config_path) as config_file:
        config_file = json.load(config_file)

    download_path = config_file['download_path']
    
    if os.path.exists(download_path) and os.path.isdir(download_path):
        Paths.download_path = download_path
        return True

    elif download_path == "":
        while True:
            user_data_path = input("\n\tWhere you want to store downloaded files (write a path here) : ")
            if (user_data_path == ""):
                print("Setting up download dir as project directory")
                download_path = Paths.download_path
                if not os.path.exists(download_path):
                    os.mkdir(download_path)

                with open(Paths.config_path, 'w') as config_file:
                    json.dump({"download_path": download_path}, config_file, indent=4, ensure_ascii=False) 
                
                Paths.download_path = download_path

                return True
                
            elif os.path.exists(user_data_path) or os.path.exists(user_data_path[1:-1]) or os.path.exists(user_data_path[1:-2]):
                if os.path.exists(user_data_path[1:-1]):
                    user_data_path = user_data_path[1:-1]
                elif os.path.exists(user_data_path[1:-2]):
                    user_data_path = user_data_path[1:-2]

                if os.path.isfile(user_data_path):
                    print("Path must be directory")
                elif os.path.isdir(user_data_path):
                    # make json file passwords.json
                    download_path = user_data_path
                    with open(Paths.config_path, 'w') as config_file:
                        json.dump({"download_path": download_path}, config_file, indent=4, ensure_ascii=False) 
                    
                    Paths.download_path = download_path
                    
                    return True
                else:
                    print("\n\tInvalid path...\n")
            else:
                print("\n\tPath not exist\n")
    
    else:
        print(download_path + " is not valid path so clearning in config path")
        return False
    

def set_gecko_path():
    platform_name = system()

    if platform_name not in ["Darwin", "Linux", "Windows"]:
        print(platform_name + " is not capatible os for this project")
        exit()

    if platform_name == "Linux":
        Paths.gecko_path = os.path.join(Paths.gecko_path, "linux", "geckodriver")
    elif platform_name == "Darwin":
        Paths.gecko_path = os.path.join(Paths.gecko_path, "macos", "geckodriver")
    else:
        Paths.gecko_path = os.path.join(Paths.gecko_path, "windows", "geckodriver.exe")

    if not os.path.exists(Paths.gecko_path):
        print("Unable to find geckodriver path : " + Paths.gecko_path)
        exit()
        