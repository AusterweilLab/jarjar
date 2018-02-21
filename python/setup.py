from setuptools import setup

setup(name='jarjar',
      version='2.1',
      description='Programatically send messages to your slack team',
      url='https://github.com/AusterweilLab/jarjar',
      author='The Austerweil Lab at UW-Madison',
      author_email='austerweil.lab@gmail.com',
      license='MIT',
      keywords=['slack', 'messaging'],
      packages=['jarjar'],
      install_requires = ['requests>=2'],
      classifiers=[
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
      ]
      )
