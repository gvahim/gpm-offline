import os
import scapy

try:
    from utils import notifier
except ImportError:
    import contextlib
    
    @contextlib.contextmanager
    def notifier(*args):
        print ' '.join(args[::-1])
        yield
        print 'D O N E'


def patch():
    with notifier('scapy', 'Fixing'):
        directory, _ = scapy.__file__.rsplit(os.sep, 1)

        file_path = os.path.join(directory, 'arch', 'windows', 'compatibility.py')

        print 'fixing the file', file_path

        with open(file_path, 'r+') as f:
            addition = [
                "from scapy.error import Scapy_Exception, log_loading, log_runtime", os.linesep,
                "from scapy.base_classes import Gen, SetGen", os.linesep,
                "import scapy.plist as plist", os.linesep,
                "from scapy.utils import PcapReader", os.linesep,
                "from scapy.data import MTU, ETH_P_ARP, ETH_P_ALL", os.linesep,
                "from scapy.arch.pcapdnet import PcapTimeoutElapsed", os.linesep,
                "import os, re, sys, socket, time, itertools", os.linesep,
                "WINDOWS = True", os.linesep
            ]

            lines = f.readlines()
            index = 0
            found = 0
            for line in lines:
                if line.startswith('import') or line.startswith('from'):
                    found += 1
                index += 1

                if found == 2:
                    break

            lines = lines[:index] + addition + lines[index:]
            f.seek(0, 0)
            f.writelines(lines)

if __name__ == '__main__':
    patch()
