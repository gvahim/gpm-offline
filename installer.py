import os
import argparse
import ctypes

from colorama import init, Fore

stage = -1

INSTALLER_VERSION = '1.0'
INSTALLER_TITLE = 'Gvahim Package Installer - v{}'.format(INSTALLER_VERSION)
SCREEN = """
/*------------------------------------------------------------------*\\
^|                       - [ Stage {stage:3d} ] -
^|                   _________________________
^|
^|                     Initial Install Script
^|                   _________________________
^|
^|                     * {t1}
^|                     *     
^|                     * {t2}    
^|                   _________________________
^|                   *** {t3} ***
^|                                                        _\^|/_
^|                                                        (o o)
\*----------------------------------------------------oOO-{{_}}-OOo---*/
"""


def display(t1, t2, t3, *args):
    """
    display screen
    :param t1: title1
    :type t1: str
    :param t2: title2
    :type t2: str
    :param t3: title3
    :type t3: str
    :param args: 
    """
    os.system('cls')
    t3 = t3.center(17)
    print Fore.LIGHTGREEN_EX + SCREEN.format(stage=stage, t1=t1, t2=t2, t3=t3),
    print os.linesep.join(map(str, args))


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
    display('', '', '')

    raw_input()

    display('ori', 'levi', 'foo', 1, 2, 3)

    raw_input()

    for k, v in Fore.__dict__.iteritems():
        print '{}: {}ori'.format(k, v)
