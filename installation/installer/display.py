import os
from colorama import Fore

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


class InvalidTitle3Error(Exception):
    def __init__(self, title):
        super(InvalidTitle3Error, self).__init__("Title3 must be 'info' or 'error' got %s" % title)


def display(stage, t1, t2, t3):
    """
    display screen
    :param stage: stage number
    :type stage: int
    :param t1: title1
    :type t1: str
    :param t2: title2
    :type t2: str
    :param t3: title3
    :type t3: str
    """
    os.system('cls')
    t3 = t3.lower()
    if t3 not in ('info', 'error'):
        raise InvalidTitle3Error(t3)

    t3 = '[{}] {}'.format(t3[0], t3.upper())
    t3 = t3.center(17)
    print Fore.LIGHTGREEN_EX + SCREEN.format(stage=stage, t1=t1, t2=t2, t3=t3).strip()
