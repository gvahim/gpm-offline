import os
import pip
import shutil
import subprocess
from colorama import Fore
from utils import create_shortcut, is_64bit_machine, install_notifier

INSTALLATION_DIR = os.path.join(os.getcwd(), 'installation')
PYTHON_INSTALLATION_DIR = os.path.join(INSTALLATION_DIR, 'python')
NETWORKS_INSTALLATION_DIR = os.path.join(INSTALLATION_DIR, 'networks')


# def uninstall_heights():
#     dirs = filter(lambda a: 'heights' == a.lower(), os.listdir('c:\\'))
#     if len(dirs) == 1:
#         path = r'c:\{}'.format(dirs[0])
#
#         with open('answes.txt', 'w') as f:
#
#
#         files = os.listdir(path)
#         if 'first.bat' not in files:
#             subprocess.call()
#
#         shutil.rmtree(path)
#
#
#     # :removeOldInstall
#     # set / a
#     # sstage += 1
#     # call:Display
#     # "Uinstall old gvahim installation" "Uninstalling..." "[i] INFO" % sstage %
#     # "C:\Heights\PortableApps\InitialSetup\untested_uninstall.bat"
#     # rmdir / S / Q
#     # "C:\Heights\PortableApps\"
#     # del "C:\Heights\Start.exe"
#     # if exist "C:\Heights\first.bat" (
#     # del "C:\Heights\first.*"
#     # )
#     # echo
#     # Delete
#     # Heights
#     # folder, keep
#     # Documents
#     # folder(C:\Heights\Documents)
#     # net
#     # session > nul
#     # 2 > & 1
#     raise NotImplementedError()


def install_pycharm():
    installation_path = os.path.join(os.getcwd(), 'pycharm')
    cmd = '{} /S /D={}'.format(os.path.join(PYTHON_INSTALLATION_DIR, 'pycharm-community-2017.1.exe'),
                               installation_path)

    with install_notifier('PyCharm 2017.1'):
        subprocess.call(cmd.split())

    exe_name = 'pycharm'
    if is_64bit_machine():
        exe_name = '{}64'.format(exe_name)
    else:
        print 'Detecting 32bit system...'
        print 'Need to install Java jre...'

        cmd = '{} /s' .format(os.path.join(PYTHON_INSTALLATION_DIR, 'jre-8u121-windows-i586.exe'))
        with install_notifier('Java jre'):
            subprocess.call(cmd.split())

    exe_name = '{}.exe'.format(exe_name)
    exe_path = os.path.join(installation_path, 'bin', exe_name)
    create_shortcut('PyCharm', exe_path)


def install_vcpy27():
    cmd = 'msiexec /i "{}" /quiet /passive'.format(os.path.join(PYTHON_INSTALLATION_DIR, 'VCForPython27.msi'))

    with install_notifier('Visual C++ Compiler for Python 2.7'):
        subprocess.call(cmd.split())


def install_python_packages():
    packages_file = os.path.join(PYTHON_INSTALLATION_DIR, 'python.packages')
    cache_dir = os.path.join(PYTHON_INSTALLATION_DIR, 'cache')
    with open(packages_file) as f:
        for package in f:
            cmd = '--find-links={} --no-index -q {}'.format(cache_dir, package)
            with install_notifier('Python Package - {}'.format(package)):
                pip.main(cmd.split())


def install_networks_packages():
    packages_file = os.path.join(NETWORKS_INSTALLATION_DIR, 'networks.packages')
    cache_dir = os.path.join(NETWORKS_INSTALLATION_DIR, 'cache')
    with open(packages_file) as f:
        for package in f:
            cmd = '--find-links={} --no-index -q {}'.format(cache_dir, package)
            with install_notifier('Python Package for Networks - {}'.format(package)):
                pip.main(cmd.split())


def install_winpcap():
    cmd = os.path.join(NETWORKS_INSTALLATION_DIR, 'WinPcap_4_1_3.exe')

    with install_notifier('WinPcap 4.1.3'):
        subprocess.call(cmd.split())


def install_wireshark():
    installation_path = os.path.join(os.getcwd(), 'wireshark')
    cmd = '{} /S /D={}'.format(os.path.join(NETWORKS_INSTALLATION_DIR, 'Wireshark-win32-2.2.5.exe'),
                               installation_path)

    with install_notifier('Wireshark 2.2.5'):
        subprocess.call(cmd.split())

    exe_path = os.path.join(installation_path, 'Wireshark.exe')
    create_shortcut('Wireshark', exe_path)


def test_everything_is_good():
    raise NotImplementedError()
