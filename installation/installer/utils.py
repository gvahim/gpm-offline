import os
import platform
import subprocess
from contextlib import contextmanager
from colorama import Fore

SHORTCUT = INSTALLATION_DIR = os.path.join(os.getcwd(), 'installation', 'Shortcut.exe')
DESKTOP_DIR = os.path.join(os.path.expanduser('~'), 'Desktop')


def create_shortcut(shortcut_name, path):
    print '[i] Creating shortcut for {}'.format(shortcut_name),
    cmd = '{} /A:C /F:{}\\{}.lnk /T:{}'.format(SHORTCUT, DESKTOP_DIR, shortcut_name, path)
    subprocess.call(cmd.split())
    print '{}[D O N E]'.format(Fore.LIGHTMAGENTA_EX)


def is_valid_os():
    """
    :return: if os version is windows 7 and above
    :rtype: bool
    """
    raise NotImplementedError()


def is_64bit_machine():
    """    
    :return: return true if the machine is 64bit otherwise return false.
    :rtype: bool
    """
    return platform.machine().endswith('64')


@contextmanager
def install_notifier(name):
    print '[i] installing {}...'.format(name),

    yield

    print '{}[D O N E]'.format(Fore.LIGHTMAGENTA_EX)


if __name__ == '__main__':
    create_shortcut('ori', 'c:\python27\python.exe')
