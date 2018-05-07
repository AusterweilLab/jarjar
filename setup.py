from setuptools import setup, find_packages
import re

# https://stackoverflow.com/a/7071358/353278
VERSIONFILE="jarjar/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(name='jarjar',
      version=verstr,
      description='Programatically send messages to your slack team',
      url='https://github.com/AusterweilLab/jarjar',
      author='The Austerweil Lab at UW-Madison',
      author_email='austerweil.lab@gmail.com',
      license='MIT',
      keywords=['slack', 'messaging'],
      packages=find_packages('.'),
      install_requires=['requests>=2'],
      zip_safe=False,
      classifiers=[
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
      ],
      data_files=[
        ('/usr/local/bin', ['bin/jarjar'])
        ]
      )
