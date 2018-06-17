from setuptools import setup
from setuptools import find_packages
import re


# get jarjar version
# https://stackoverflow.com/a/7071358/353278
VERSIONFILE = "jarjar/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

long_description = '\
Jarjar is a python utility that makes it easy to send slack notifications \
to your teams. You can import it as a python module or use our command \
line tool.'

# install jarjar
setup(
    name='jarjar',
    version=verstr,
    description='Use python to send messages to your slack team',
    long_description=long_description,
    url='https://github.com/AusterweilLab/jarjar',
    author='The Austerweil Lab at UW-Madison',
    author_email='austerweil.lab@gmail.com',
    license='MIT',
    keywords=['slack', 'messaging'],
    packages=find_packages('.'),
    install_requires=['requests'],
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    scripts=['bin/jarjar'],
)
