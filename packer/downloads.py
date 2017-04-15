import os
import pip
import urllib
import requests

from colorama import Fore
from utils import fix_width
from contextlib import contextmanager
from hurry.filesize import size, alternative


@contextmanager
def download_notifier(name):
    print fix_width('Downloading {}...'.format(name)),
    yield
    print '{}[D O N E]'.format(Fore.LIGHTMAGENTA_EX)


def pip_download(package_):
    cmd = 'download {} -q'.format(package_)
    with download_notifier(package_):
        pip.main(cmd.split())


def download_file(name, url, software_dir_):
    def report_download(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        equal = int(percent * 0.7)
        print '\r\t{file_name} ({size}) [{equal}>{space}] {percent}%'.format(
            percent=percent, equal='=' * equal,
            space=' ' * (70 - equal),
            size=size(total_size, alternative),
            file_name=name),

    print 'Downloading {} from {}...'.format(name, url)
    filename, file_extension = os.path.splitext(url)
    save_path = os.path.join(software_dir_, '{}{}'.format(name, file_extension))
    urllib.urlretrieve(url, save_path, report_download)
    print
    return save_path


def download_string(url, as_json=False):
    res = requests.get(url)
    res.raise_for_status()
    if as_json:
        return res.json()
    return res.text

