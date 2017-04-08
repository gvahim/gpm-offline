import ctypes
import argparse

from colorama import init
from installer.steps import *
from installer.display import display

INSTALLER_VERSION = '1.0'
INSTALLER_TITLE = 'Gvahim Package Installer - v{}'.format(INSTALLER_VERSION)

STEPS = (
    # ('Uninstall Old Heights Installation', 'Uninstalling...', uninstall_heights),
    ('Install Visual C++ Compiler for Python', 'Ininstalling...', install_vcpy27),
    ('Install Python Packages', 'Ininstalling...', install_python_packages),
    ('Install PyCharm', 'Ininstalling...', install_pycharm),
    ('Install WinPcap', 'Ininstalling...', install_winpcap),
    ('Install WireShark', 'Ininstalling...', install_wireshark),
    ('Install Networks Packages', 'Ininstalling...', install_networks_packages),
    # ('Set the environment path', '', setting_path),
    ('Install Tests', 'Testing...', test_everything_is_good)
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

    for i, (step_title, step_subtitle, step_func) in enumerate(STEPS, 1):
        display(stage + i, step_title, step_subtitle, "info")
        step_func()

    stage += len(STEPS)
    exit(stage)
