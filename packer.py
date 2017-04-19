import os
import pip
import urllib
import shutil
import hashlib
import argparse

from colorama import init, Fore
from contextlib import contextmanager
from hurry.filesize import size, alternative

INSTALLATION_DIR = 'installation'
WINRAR = r'C:\Program Files (x86)\WinRAR\rar.exe'

PACKAGES = {
    'packages': ['colorama', 'pip'],
    'requirements': [os.path.join('..', 'python.packages'),
                     os.path.join('..', 'networks.packages')]
}

GENERAL_SOFTWARES = {
    'WinPcap': (
        'https://www.winpcap.org/install/bin/WinPcap_4_1_3.exe',
        'fc4623b113a1f603c0d9ad5f83130bd6de1c62b973be9892305132389c8588de'
    ),
    'PyCharm': (
        'https://download.jetbrains.com/python/pycharm-community-2017.1.1.exe',
        'dc7ea70fa2b34721f939c641294ec68f9ed05355ffbf32bb11d622ddad232861'
    ),
    'VCForPython27': (
        'https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-'
        'B59FBF6D907B/VCForPython27.msi',
        '070474db76a2e625513a5835df4595df9324d820f9cc97eab2a596dcbc2f5cbf')
}

SOFTWARES_32BIT = {
    'Wireshark': (
        'https://1.as.dl.wireshark.org/win32/Wireshark-win32-2.2.6.exee',
        'd43a3194d4cb6899bda39fb24e43bbfd8497d6c2794658f69955b7d6a111a796'
    ),
    'python': (
        'https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi',
        '44ea95356365195b18a5058796285789b0bfc94da1ee2ec1cb8e0a1c2ff6017a'
    )
}

SOFTWARES_64BIT = {
    'Wireshark': (
        'https://1.as.dl.wireshark.org/win64/Wireshark-win64-2.2.6.exe',
        'faa10fe979440aa231478b8ad35ae5810020f814438e735e6edd57611465c405'
    ),
    'python': (
        'https://www.python.org/ftp/python/2.7.13/python-2.7.13.amd64.msi',
        '8b3e65fc1aad8809bb69477e922c3609a8e8fa9e2f6d5ab8f00f3553e3c61d7a'
    )
}


@contextmanager
def download_notifier(name):
    print fix_width('Downloading {}...'.format(name)),
    yield
    print '{}[D O N E]'.format(Fore.LIGHTMAGENTA_EX)


def fix_width(message, width=65):
    fmt = '{{:{}}}'.format(width)
    return fmt.format(message)


@contextmanager
def change_directory(path_):
    save = os.getcwd()
    os.chdir(path_)
    yield
    os.chdir(save)


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


def create_empty_directory(path_):
    if os.path.exists(path_):
        shutil.rmtree(path_)
    os.mkdir(path_)


def calculate_sha256(path_):
    with open(path_, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


if __name__ == '__main__':
    init(autoreset=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--machine64', action='store_true')
    parser.add_argument('-c', '--check-sum', nargs='+',
                        help='Use this option to calculate check sum')

    args = parser.parse_args()

    if args.check_sum:
        for software in args.check_sum:
            print 'Check sum for {}: {}'.format(software,
                                                calculate_sha256(software))

    else:
        for directory in ('cache', 'softwares'):
            path = os.path.join(INSTALLATION_DIR, directory)
            if os.path.exists(path):
                shutil.rmtree(path)

        directory = 'gvahim{}'.format('_64bit' if args.machine64 else '')
        create_empty_directory(directory)
        shutil.copyfile('install.cmd', os.path.join(directory, 'install.cmd'))
        shutil.copytree(INSTALLATION_DIR,
                        os.path.join(directory, INSTALLATION_DIR))
        if args.machine64:
            os.remove(os.path.join('gvahim_64bit', INSTALLATION_DIR,
                                   'jre-8u121-windows-i586.exe'))

        download_file('get-pip', 'https://bootstrap.pypa.io/get-pip.py',
                      os.path.join(directory, INSTALLATION_DIR))

        cache_dir = os.path.join(directory, INSTALLATION_DIR, 'cache')
        software_dir = os.path.join(directory, INSTALLATION_DIR, 'softwares')

        create_empty_directory(cache_dir)
        with change_directory(cache_dir):
            for package in PACKAGES['packages']:
                pip_download(package)

            for requirement in PACKAGES['requirements']:
                with open(requirement) as file_:
                    for package in file_:
                        if package.startswith('#'):
                            continue
                        package = package.strip()
                        pip_download(package)

        create_empty_directory(software_dir)
        softwares = [GENERAL_SOFTWARES]
        if args.machine64:
            softwares.append(SOFTWARES_64BIT)
        else:
            softwares.append(SOFTWARES_32BIT)

        for software in softwares:
            for name_, (url_, hash_) in software.iteritems():
                path = download_file(name_, url_, software_dir)
                calc_hash = calculate_sha256(path)
                if hash_ == calc_hash:
                    color = Fore.GREEN
                    msg = 'O K'
                else:
                    color = Fore.RED
                    msg = 'E R R O R'
                msg_ = '{} - Verify download ... '.format(name_)
                print '{}{}[{}]'.format(fix_width(msg_), color, msg)
