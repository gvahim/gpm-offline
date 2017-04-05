import ctypes
import argparse

from colorama import init
from installer.steps import *
from installer.display import display

INSTALLER_VERSION = '1.0'
INSTALLER_TITLE = 'Gvahim Package Installer - v{}'.format(INSTALLER_VERSION)

STEPS = (
    ('Visual C++ Compiler for Python', install_vcpy27),
    ('Python Packages', install_python_packages),
    ('PyCharm', install_pycharm),
    ('WinPcap', install_winpcap),
    ('WireShark', install_wireshark),
    ('Install Tests', test_everything_is_good)
)


def init_display():
    ctypes.windll.kernel32.SetConsoleTitleA(INSTALLER_TITLE)
    init(autoreset=True)

if __name__ == '__main__':
    init_display()

    parser = argparse.ArgumentParser()
    parser.add_argument('stage', type=int)

    args = parser.parse_args()

    stage = args.stage

    for i, (step_title, step_func) in enumerate(STEPS, 1):
        display(stage + i, 'Install {}'.format(step_title), "installing...", "info")
        step_func()

    stage += len(STEPS)
    exit(stage)
