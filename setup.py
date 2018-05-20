from setuptools.command.install import install
from setuptools import setup
from setuptools import find_packages
from setuptools import Distribution
import re


class OnlyGetScriptPath(install):
	"""Class to enable bin install location.

	see https://stackoverflow.com/a/25176606/353278
	"""

	def run(self):
		"""Necessary method for setuptools."""
		# does not call install.run() by design
		self.distribution.install_scripts = self.install_scripts


def get_setuptools_script_dir():
	"""Determine the script dir that setuptools would save in.

	see https://stackoverflow.com/a/25176606/353278
	"""
	dist = Distribution({'cmdclass': {'install': OnlyGetScriptPath}})
	dist.dry_run = True  # not sure if necessary, but to be safe
	dist.parse_config_files()
	command = dist.get_command_obj('install')
	command.ensure_finalized()
	command.run()
	return dist.install_scripts


jarjar_dir = get_setuptools_script_dir()

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

# install jarjar
setup(
	name='jarjar',
	version=verstr,
	description='Programatically send messages to your slack team',
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
	data_files=[(jarjar_dir, ['bin/jarjar'])]
)
