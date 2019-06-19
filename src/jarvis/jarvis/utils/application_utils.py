import sys
import os
import time
import requests
import traceback
import logging

from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
from subprocess import call
from logging import config

from jarvis.utils import response_utils
from jarvis.settings import LOG_SETTINGS
from jarvis._version import __version__

jarvis_logo = "\n"\
"      ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗\n"\
"      ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝\n"\
"      ██║███████║██████╔╝██║   ██║██║███████╗\n"\
" ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║\n"\
" ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║\n"\
"  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝"


start_text = "" \
" -----------------------------------------------\n"\
" -  Voice Assistant Platform  " + "v" +  __version__ + "   -\n"\
" -----------------------------------------------\n"


class OutputStyler:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    CYAN = '\033[36m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


user_input = OutputStyler.CYAN + '>> ' + OutputStyler.ENDC

# Create a Console & Rotating file logger
config.dictConfig(LOG_SETTINGS)


def log(func):
    """
    Logging wrapper
    :param func: function object
    """
    def wrapper(*args, **kwargs):
        try:
            logging.debug(func.__name__)
            func(*args, **kwargs)
        except Exception:
            logging.error(func.__name__)
            traceback.print_exc(file=sys.stdout)
    return wrapper


def clear():
    """
    Clear stdout
    """
    _ = call('clear' if os.name == 'posix' else 'cls')  # check and make call for specific operating system


def internet_connectivity_check(url='http://www.google.com/', timeout=2):
    """
    Checks for internet connection availability based on google page.
    """
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        logging.info("No internet connection.")
        return False


def startup_ckecks():
    """
    Initial checks
    """

    print("=" * 48)
    print("Startup ckeck")
    print("=" * 48)

    print("INFO: Internet connection check..")
    if not internet_connectivity_check():
        response_utils.stdout_print("WARNING: No internet connection, skills with internet connection will not work")
        time.sleep(3)


def start_up():
    """
    Do initial checks, clear the console and print the assistant logo.
    """
    startup_ckecks()
    clear()
    print(OutputStyler.CYAN + jarvis_logo + OutputStyler.ENDC)
    print(OutputStyler.HEADER + start_text + OutputStyler.ENDC)

    logging.info('\n' + '#'*50 + '\n' + 'APPLICATION STARTS - ' + str(datetime.now()) + '\n' + '#'*50)


def play_activation_sound():
    """
    Plays a sound when the assistant enables.
    """
    utils_dir = os.path.dirname(__file__)
    enable_sound = os.path.join(utils_dir, '..', 'files', 'enable_sound.wav')
    song = AudioSegment.from_wav(enable_sound)
    play(song)