import os
import pip
import shutil
import _winreg
import importlib
import subprocess
from colorama import Fore
from utils import create_shortcut, is_64bit_machine, notifier, heights_path, fix_width, DESKTOP_DIR

INSTALLATION_DIR = os.path.join(os.getcwd(), 'installation')
SOFTWARES_DIR = os.path.join(INSTALLATION_DIR, 'softwares')
CACHE_DIRECTORY = os.path.join(INSTALLATION_DIR, 'cache')


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
                with notifier(msg, '', True):
                    func(del_path)

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
    cmd = '{} /S /D={}'.format(os.path.join(SOFTWARES_DIR, 'PyCharm.exe'),
                               installation_path)

    with notifier('PyCharm 2017.1'):
        subprocess.call(cmd.split())

    exe_name = 'pycharm'
    if is_64bit_machine():
        exe_name = '{}64'.format(exe_name)
    else:
        print 'Detecting 32bit system...'
        print 'Need to install Java jre...'

        cmd = '{} /s' .format(os.path.join(INSTALLATION_DIR, 'jre-8u121-windows-i586.exe'))
        with notifier('Java jre'):
            subprocess.call(cmd.split())

    exe_name = '{}.exe'.format(exe_name)
    exe_path = os.path.join(installation_path, 'bin', exe_name)
    create_shortcut('PyCharm', exe_path)


def install_vcpy27():
    cmd = 'msiexec /i "{}" /quiet /passive'.format(os.path.join(SOFTWARES_DIR, 'VCForPython27.msi'))

    with notifier('Visual C++ Compiler for Python 2.7'):
        subprocess.call(cmd.split())


def install_with_pip(packages_file, notifier_title):
    with open(packages_file) as f:
        for package in f:
            if package.startswith('#'):
                continue
            package = package.strip()
            cmd = 'install --find-links={} --no-index -q {}'.format(CACHE_DIRECTORY, package)
            with notifier('{} - {}'.format(notifier_title, package)):
                pip.main(cmd.split())


def install_python_packages():
    packages_file = os.path.join(INSTALLATION_DIR, 'python.packages')
    install_with_pip(packages_file, 'Python Package')


def install_networks_packages():
    packages_file = os.path.join(INSTALLATION_DIR, 'networks.packages')
    install_with_pip(packages_file, 'Python Package for Networks')


def install_winpcap():
    cmd = os.path.join(SOFTWARES_DIR, 'WinPcap.exe')

    with notifier('WinPcap 4.1.3'):
        subprocess.call(cmd.split())


def install_wireshark():
    installation_path = os.path.join(os.getcwd(), 'wireshark')
    cmd = '{} /S /D={}'.format(os.path.join(SOFTWARES_DIR, 'Wireshark.exe'),
                               installation_path)

    with notifier('Wireshark 2.2.5'):
        subprocess.call(cmd.split())

    with notifier('Setting up WIRESHARKPATH environment variable', ''):
        cmd = 'setx WIRESHARKPATH "{}" /m > nul'.format(installation_path)
        subprocess.call(cmd.split())

    exe_path = os.path.join(installation_path, 'Wireshark.exe')
    create_shortcut('Wireshark', exe_path)


def set_environment_variable():
    def read_system_environment_variable(name='path'):
        k = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')
        value, type_ = _winreg.QueryValueEx(k, name)
        _winreg.CloseKey(k)
        return value

    path = read_system_environment_variable()
    cmd = 'setx PATH "%PATH%;%{}%" /m > nul'

    for variable in ('PYTHONPATH', 'WIRESHARKPATH'):
        full_name = '%{}%'.format(variable)
        if full_name not in path:
            with notifier('Adding {} to PATH'.format(variable)):
                subprocess.call(cmd.format(variable).split())


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
        os.path.join(INSTALLATION_DIR, 'python.packages'),
        os.path.join(INSTALLATION_DIR, 'networks.packages')
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