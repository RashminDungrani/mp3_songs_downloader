""" Path of all data files """

from os.path import join
from pathlib import Path

class Paths:
    ''' Just Location of useful data files '''

    proj_dir = Path(__file__).parent.parent

    requirement_path = join(proj_dir, "requirements.txt")

    gecko_path = join(proj_dir, "geckodriver")

    config_path = join(proj_dir, "config.json")

    download_path = join(proj_dir, "downloads")
    