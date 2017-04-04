import os
import ctypes

from colorama import init, Fore

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


def display(stage, t1, t2, t3, *args):
    """
    display screen
    :param stage: the stage number
    :type stage: int
    :param t1: title1
    :type t1: str
    :param t2: title2
    :type t2: str
    :param t3: title3
    :type t3: str
    :param args: 
    """
    print Fore.LIGHTGREEN_EX + SCREEN.format(stage=stage, t1=t1, t2=t2, t3=t3),
    print os.linesep.join(map(str, args))


def is_valid_os():
    """
    :return: if os version is windows 7 and above
    :rtype: bool
    """
    raise NotImplementedError()

if __name__ == '__main__':
    ctypes.windll.kernel32.SetConsoleTitleA(INSTALLER_TITLE)

    init(autoreset=True)

    display(1, 'ori', 'levi', 'foo', 1, 2, 3)

    raw_input()

    for k, v in Fore.__dict__.iteritems():
        print '{}: {}ori'.format(k, v)
