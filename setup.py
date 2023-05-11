from setuptools import setup
import os
with open('requirements.txt') as f:
    required = f.read().splitlines()
setup(
   name='FIXRobot',
   version='1.0',
   description='A useful module to test FIX connectivity and FIX engines. Usage: import FIXRobot',
   license="MIT",
   long_description='A useful module to test FIX connectivity and FIX engines. Usage: import FIXRobot',
   author='Man Foo',
   author_email='quickfixrobot@gmail.com',
   url="https://github.com/quickfixrobot",
   packages=['FIXRobot'],  #same as name
   install_requires=required, #external packages as dependencies
   scripts=[
            'scripts/cool',
            'scripts/skype',
           ]
)
