import os
import winshell


def create_shortcut(shortcut_name, path, description=None):

    shortcut_name = '{}.lnk'.format(shortcut_name)
    link_file_path = os.path.join(winshell.desktop(), shortcut_name)
    with winshell.shortcut(link_file_path) as link:
        link.path = path
        if description:
            link.description = description


def is_valid_os():
    """
    :return: if os version is windows 7 and above
    :rtype: bool
    """
    raise NotImplementedError()


if __name__ == '__main__':
    create_shortcut('ori', 'c:\python27\python.exe')
