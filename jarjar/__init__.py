from sys import version_info as _version_info

if isinstance(_version_info, tuple):
    version = _version_info[0]
else:
    version = _version_info.major

# different importing for python 2 and 3
if version == 2:
    from jarjar import jarjar
    from _version import __version__
    from screen import Screen
else:
    from jarjar.jarjar import jarjar
    from jarjar._version import __version__
    from jarjar.screen import Screen

__all__ = [
    '__version__',
    'Screen',
    'jarjar',
]
