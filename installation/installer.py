import argparse
import ctypes
import installer.display

from colorama import init, Fore

INSTALLER_VERSION = '1.0'
INSTALLER_TITLE = 'Gvahim Package Installer - v{}'.format(INSTALLER_VERSION)


def is_valid_os():
    """
    :return: if os version is windows 7 and above
    :rtype: bool
    """
    raise NotImplementedError()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', type=int)

    args = parser.parse_args()

    stage = args.stage

    ctypes.windll.kernel32.SetConsoleTitleA(INSTALLER_TITLE)
    init(autoreset=True)

    stage = 1
    installer.display.display(0, '', '', 'info')

    raw_input()

    installer.display.display(1, 'ori', 'levi', 'error', 1, 2, 3)

    raw_input()

    for k, v in Fore.__dict__.iteritems():
        print '{}: {}ori'.format(k, v)

    exit(stage)
