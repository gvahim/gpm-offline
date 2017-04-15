import os
import shutil
import argparse

from colorama import init, Fore
from downloads import pip_download, download_file, download_string
from utils import (calculate_sha256, create_empty_directory,
                   change_directory, fix_width)

INSTALLATION_DIR = 'installation'
WINRAR = r'C:\Program Files (x86)\WinRAR\rar.exe'

SOFTWARES = 'https://raw.githubusercontent.com/gvahim/gpm-offline/master/packer/softwares.json'
PYTHON_PACKAGES = 'https://raw.githubusercontent.com/gvahim/gpm-offline/master/installation/python.packages'
NETWORKS_PACKAGES = 'https://raw.githubusercontent.com/gvahim/gpm-offline/master/installation/networks.packages'
PACKAGES = ['colorama']


def handle_check_sum_only(files):
    for software in files:
        software_hash = calculate_sha256(software)
        print 'Check sum for {}: {}'.format(software, software_hash)


def handle_pip_packages(parent_directory):
    cache_dir = os.path.join(parent_directory, INSTALLATION_DIR, 'cache')
    create_empty_directory(cache_dir)

    with change_directory(cache_dir):
        packages = PACKAGES[:]
        packages.extend(download_string(PYTHON_PACKAGES.split('\n')))
        packages.extend(download_string(NETWORKS_PACKAGES.split('\n')))

        packages = filter(lambda pack: not pack.startswith('#'), packages)

        for package in packages:
            pip_download(package)


def handle_softwares(parent_directory, is64bit):
    software_dir = os.path.join(parent_directory, INSTALLATION_DIR, 'softwares')
    # create_empty_directory(software_dir)

    softwares = download_string(SOFTWARES, True)
    keys = ('General', '64bit' if is64bit else '32bit')

    for key in keys:
        for name, v in softwares[key].iteritems():
            url, hash_ = v['url'], v['hash']

            path = download_file(name, url, software_dir)
            calculated_hash = calculate_sha256(path)
            if hash_ == calculated_hash:
                color = Fore.GREEN
                msg = 'O K'
            else:
                color = Fore.RED
                msg = 'E R R O R'
            msg_ = '{} - Verify download ... '.format(name)
            print '{}{}[{}]'.format(fix_width(msg_), color, msg)


if __name__ == '__main__':
    init(autoreset=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--machine64', action='store_true')
    parser.add_argument('-c', '--check-sum', nargs='+',
                        help='Use this option to calculate check sum')

    args = parser.parse_args()

    if args.check_sum:
        handle_check_sum_only(args.check_sum)
    else:
        for directory in ('cache', 'softwares'):
            path = os.path.join(INSTALLATION_DIR, directory)
            if os.path.exists(path):
                shutil.rmtree(path)

        # TODO: check this!
        directory_name = 'gvahim{}'.format('_64bit' if args.machine64 else '')
        directory = os.path.join('..', directory_name)

        create_empty_directory(directory)
        shutil.copyfile('install.cmd', os.path.join(directory, 'install.cmd'))
        shutil.copytree(INSTALLATION_DIR,
                        os.path.join(directory, INSTALLATION_DIR))
        if args.machine64:
            os.remove(os.path.join('gvahim_64bit', INSTALLATION_DIR,
                                   'jre-8u121-windows-i586.exe'))

        handle_pip_packages(directory)
        handle_softwares(directory, args.machine64)
