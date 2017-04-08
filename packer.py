import os
import urllib
import argparse
import pip
import subprocess
from colorama import init, Fore
from contextlib import contextmanager
from hurry.filesize import size, alternative

INSTALLATION_DIR = 'installation'
CACHE_DIR = os.path.join(INSTALLATION_DIR, 'cache')
SOFTWARES_DIR = os.path.join(INSTALLATION_DIR, 'softwares')
WINRAR = r'C:\Program Files (x86)\WinRAR\rar.exe'

PACKAGES = {
    'packages': ['colorama'],
    'requirements': [os.path.join('..', 'python', 'python.packages'),
                     os.path.join('..', 'networks', 'networks.packages')]
}

GENERAL_SOFTWARES = {
    'WinPcap': 'https://www.winpcap.org/install/bin/WinPcap_4_1_3.exe',
    'PyCharm': 'https://download.jetbrains.com/python/pycharm-professional-2017.1.exe',
    'VCForPython27': 'https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi'
}

SOFTWARES_32BIT = {
    'Wireshark32': 'https://1.as.dl.wireshark.org/win32/Wireshark-win32-2.2.5.exe',
    'JRE32': 'http://download.oracle.com/otn-pub/java/jdk/8u121-b13/e9e7ea248e2c4826b92b3f075a80e441/jre-8u121-windows-i586.exe',
    'Python32': 'https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi',
}

SOFTWARES_64BIT = {
    'Wireshark64': 'https://1.as.dl.wireshark.org/win64/Wireshark-win64-2.2.5.exe',
    'Python64': 'https://www.python.org/ftp/python/2.7.13/python-2.7.13.amd64.msi',
}


@contextmanager
def download_notifier(name):
    msg = 'Downloading {}...'.format(name)
    print fix_width(msg),
    yield
    print '{}[D O N E]'.format(Fore.LIGHTMAGENTA_EX)


def fix_width(msg, width=65):
    fmt = '{{:{}}}'.format(width)
    return fmt.format(msg)


@contextmanager
def change_directory(path):
    save = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(save)


def pip_download(package_):
    cmd = 'download {} -q'.format(package_)
    with download_notifier(package_):
        pip.main(cmd.split())


def download_file(name, url):
    def report_download(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        equal = int(percent * 0.7)
        print '\r\t{file_name} ({size}) [{equal}>{space}] {percent}%'.format(percent=percent, equal='='*equal,
                                                                             space=' ' * (70 - equal),
                                                                             size=size(total_size, alternative),
                                                                             file_name=name)

    print 'Downloading {} from {}...'.format(name, url)
    head, tail = os.path.split(url)
    save_path = os.path.join(SOFTWARES_DIR, tail)
    urllib.urlretrieve(url, save_path, report_download)
    print

if __name__ == '__main__':
    init(autoreset=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--is64bit', action='store_true')

    args = parser.parse_args()
    print args

    with change_directory(CACHE_DIR):
        for package in PACKAGES['packages']:
            pip_download(package)

        for requirement in PACKAGES['requirements']:
            with open(requirement) as file_:
                for package in file_:
                    if package.startswith('#'):
                        continue
                    package = package.strip()
                    pip_download(package)

    softwares = [GENERAL_SOFTWARES]
    if args.is64bit:
        softwares.append(SOFTWARES_64BIT)
    else:
        softwares.append(SOFTWARES_32BIT)

    for software in softwares:
        for name_, url_ in software.iteritems():
            download_file(name_, url_)

    # # pack to sfx archive
    # cmd = '{} a -r -sfx -z"xfs.conf" auto_install install_me.exe'.format(WINRAR)
    # subprocess.call(cmd.split())
