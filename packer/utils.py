import os
import shutil
import hashlib

from contextlib import contextmanager


def fix_width(message, width=65):
    """
    print message with fix width
    :param message: what to print
    :type message: str 
    :param width: the desired width
    :type width: int 
    :return: the string with fix width
    :rtype: str
    """
    fmt = '{{:{}}}'.format(width)
    return fmt.format(message)


@contextmanager
def change_directory(path):
    """
    change directory and return to the current, use with with statement.
    :param path: the path to change
    :type path: str    
    """
    save = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(save)


def create_empty_directory(path):
    """
    Create an empty directory, if exists delete it (with content),
    and create new one.
    :param path: the path to clean
    :type path: str
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


def calculate_sha256(path):
    """
    Return the hash of a file (sha256)
    :param path: path to file
    :type path: str
    :return: the hash
    :rtype: str
    """
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()
