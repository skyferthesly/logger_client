from setuptools import setup, find_packages

setup(name='logger_client',
      packages=find_packages(exclude=['tests']),
      version='0.1',
      license='MIT',

      description='Gui client that accepts and sends user data to a configurable webservice',
      long_description=open('README.md').read(),

      url='https://github.com/skyferthesly/logger_client',

      author='Skyler Moore-Firkins',
      author_email='brehon1104@gmail.com',

      setup_requires=['pytest',
                      'requests'
                      ]
      )

# test_suite=''
