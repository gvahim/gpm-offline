import time
import ctypes
import argparse

from colorama import init
from installer.steps import *
from installer.display import display

INSTALLER_VERSION = '1.3'
INSTALLER_TITLE = 'Gvahim Package Installer - v{}'.format(INSTALLER_VERSION)

STEPS = (
    # ('Uninstall Old Heights Installation', 'Uninstalling...',
    #  uninstall_heights),
    ('Install Python Packages', 'Ininstalling...', install_python_packages),
    ('Install PyCharm', 'Ininstalling...', install_pycharm),
    ('Install WinPcap', 'Ininstalling...', install_winpcap),
    ('Install WireShark', 'Ininstalling...', install_wireshark),
    ('Install Networks Packages', 'Ininstalling...', install_networks_packages),
    ('Setting Up Environment Variables', 'Setting...',
     set_environment_variable),
    ('Install Tests', 'Testing...', test_everything_is_good)
)


def init_display():
    ctypes.windll.kernel32.SetConsoleTitleA(INSTALLER_TITLE)
    init(autoreset=True)


if __name__ == '__main__':
    init_display()

    parser = argparse.ArgumentParser()
    parser.add_argument('stage', type=int)
    parser.add_argument('-d', '--debug', action='store_true')

    args = parser.parse_args()

    stage = args.stage

    for i, (step_title, step_subtitle, step_func) in enumerate(STEPS, 1):
        display(stage + i, step_title, step_subtitle, "info")
        step_func()
        if args.debug:
            raw_input('{}[DEBUG MODE] Press any key to continue...'.format(Fore.LIGHTRED_EX))
        else:
            time.sleep(2)

    stage += len(STEPS)
    exit(stage)
