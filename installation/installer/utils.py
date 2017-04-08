import os
import platform
import subprocess
from contextlib import contextmanager
from colorama import Fore

SHORTCUT = INSTALLATION_DIR = os.path.join(os.getcwd(), 'installation', 'Shortcut.exe')
DESKTOP_DIR = os.path.join(os.path.expanduser('~'), 'Desktop')


def create_shortcut(shortcut_name, path):
    msg = '[i] Creating shortcut for {}'.format(shortcut_name)
    print '{:65}'.format(msg),
    cmd = '{} /A:C /F:{}\\{}.lnk /T:{}'.format(SHORTCUT, DESKTOP_DIR, shortcut_name, path)
    with open(os.devnull, 'w') as fnull:
        subprocess.call(cmd.split(), stdout=fnull)
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
    msg = '[i] installing {}...'.format(name)
    print '{:65}'.format(msg),
    yield
    print '{}[D O N E]'.format(Fore.LIGHTMAGENTA_EX)


if __name__ == '__main__':
    print SHORTCUT
    create_shortcut('ori', 'c:\python27\python.exe')
