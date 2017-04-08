import os
import winshell
import platform
from contextlib import contextmanager
from colorama import Fore


def create_shortcut(shortcut_name, path, description=None):

    shortcut_name = '{}.lnk'.format(shortcut_name)
    link_file_path = os.path.join(winshell.desktop(), shortcut_name)
    with winshell.shortcut(link_file_path) as link:
        link.path = path
        if description:
            link.description = description


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
