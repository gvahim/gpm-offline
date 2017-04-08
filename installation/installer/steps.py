import os
import pip
import shutil
import _winreg
import importlib
import subprocess
from colorama import Fore
from utils import create_shortcut, is_64bit_machine, install_notifier, heights_path, fix_width, DESKTOP_DIR

INSTALLATION_DIR = os.path.join(os.getcwd(), 'installation')
PYTHON_INSTALLATION_DIR = os.path.join(INSTALLATION_DIR, 'python')
NETWORKS_INSTALLATION_DIR = os.path.join(INSTALLATION_DIR, 'networks')


def uninstall_heights():

    path = heights_path()
    if not path:
        print '[i] Cannot detect old heights installation...'
    else:
        print '[i] Find old heigth installation, trying to uninstall it.'
        print 'Delete Heights Installation:'

        deletes = (
            (shutil.rmtree, 'PortableApps Directory', 'PortableApps'),
            (os.remove, 'Start.exe', 'Start.exe'),
            (os.remove, 'first.bat', 'first.bat'),
            (os.remove, 'first.vbs', 'first.vbs'),
        )

        for func, (msg, file_) in deletes:
            del_path = os.path.join(path, file_)
            if os.path.exists(del_path):
                print '\t[*]{}'.format(fix_width(msg)),
                func(del_path)
                print '{}[D O N E}'.format(Fore.LIGHTMAGENTA_EX)

        # remove shortcuts
        shortcuts = filter(lambda a: a.endswith('Heights.lnk') or a.endswith('Heights-PyCharm.lnk'),
                           os.listdir(DESKTOP_DIR))
        for shortcut in shortcuts:
            shortcut_path = os.path.join(DESKTOP_DIR, shortcut)
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)

        # remove registry keys
        keys = (
            (_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Classes\Python.File\\'),
            (_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Classes\Pythonw.File\\'),
            (_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Classes\wireshark-capture-file\\'),
            (_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\Python\PythonCore\2.7\\'),

            (_winreg.HKEY_CLASSES_ROOT, r'Pythonw.File\shell\Open with Heights Pycharm'),
            (_winreg.HKEY_CLASSES_ROOT, r'Python.File\shell\Open with Heights Pycharm'),
            (_winreg.HKEY_CLASSES_ROOT, r'Pythonw.File\shell\Open with Heights IDLE'),
            (_winreg.HKEY_CLASSES_ROOT, r'Python.File\shell\Open with Heights IDLE'),
            (_winreg.HKEY_CLASSES_ROOT, r'Pythonw.File\shell\Open with Heights Notepad++'),
            (_winreg.HKEY_CLASSES_ROOT, r'Python.File\shell\Open with Heights Notepad++'),
        )
        for key, sub_key in keys:
            _winreg.DeleteKey(key, sub_key)


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


def install_with_pip(packages_file, cache_dir, notifier_title):
    with open(packages_file) as f:
        for package in f:
            if package.startswith('#'):
                continue
            package = package.strip()
            cmd = 'install --find-links={} --no-index -q {}'.format(cache_dir, package)
            with install_notifier('{} - {}'.format(notifier_title, package)):
                pip.main(cmd.split())


def install_python_packages():
    packages_file = os.path.join(PYTHON_INSTALLATION_DIR, 'python.packages')
    cache_dir = os.path.join(PYTHON_INSTALLATION_DIR, 'cache')

    install_with_pip(packages_file, cache_dir, 'Python Package')


def install_networks_packages():
    packages_file = os.path.join(NETWORKS_INSTALLATION_DIR, 'networks.packages')
    cache_dir = os.path.join(NETWORKS_INSTALLATION_DIR, 'cache')

    install_with_pip(packages_file, cache_dir, 'Python Package for Networks')


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
    # test for:
    #   [*] python
    #   [*] python libraries
    #   [*] networks libraries
    #   [] pycharm
    #   [] wireshark

    print 'Testing the installation:'
    print '\t[*] {}'.format(fix_width('Python install {}successfully'.format(Fore.GREEN)))

    libraries_paths = (
        os.path.join(PYTHON_INSTALLATION_DIR, 'python.packages'),
        os.path.join(NETWORKS_INSTALLATION_DIR, 'networks.packages')
    )

    for libraries_path in libraries_paths:
        with open(libraries_path) as file_:
            for library in file_:
                if library.startswith('#'):
                    continue

                library = library.split()
                try:
                    importlib.import_module(library)
                    msg = '{}successfully'.format(Fore.GREEN)
                except ImportError:
                    msg = '{}failed'.format(Fore.RED)

                print '\t[*] {}'.format(fix_width('Python {} package install {}'.format(library, msg)))

    print '{}YAY everything is install! have fun'.format(Fore.LIGHTRED_EX)
    raw_input('Press any key to continue...')


if __name__ == '__main__':
    # print PYTHON_INSTALLATION_DIR
    # install_networks_packages()
    # test_everything_is_good()
    importlib.import_module('ori')