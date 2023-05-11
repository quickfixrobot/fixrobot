from setuptools import setup

import sys
import subprocess
import pkg_resources
import platform

required  = {'quickfix', 'configparser', 'pytest'}
quickfix_windows_wheels= { 'cp39-windows-amd64':'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp39‑cp39‑win_amd64.whl',
                           'cp39-windows-win32':'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp39‑cp39‑win32.whl',
                           'cp38-windows-amd64':'https://download.lfd.uci.edu/pythonlibs/archived/quickfix-1.15.1-cp38-cp38-win_amd64.whl',
                           'cp38-windows-win32':'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp38‑cp38‑win32.whl',
                           'cp37-windows-amd64': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp37‑cp37m‑win_amd64.whl',
                           'cp37-windows-win32': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp37‑cp37m‑win32.whl',
                           'cp36-windows-amd64': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp36‑cp36m‑win_amd64.whl',
                           'cp36-windows-win32': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp36‑cp36m‑win32.whl',
                           'cp35-windows-amd64': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp35‑cp35m‑win_amd64.whl',
                           'cp35-windows-win32': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp35‑cp35m‑win32.whl',
                           'cp34-windows-amd64': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp34‑cp34m‑win_amd64.whl',
                           'cp34-windows-win32': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp34‑cp34m‑win32.whl',
                           'cp27-windows-amd64': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp27‑cp27m‑win_amd64.whl',
                           'cp27-windows-win32': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.15.1‑cp27‑cp27m‑win32.whl',
                           'cp27-windows-none': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.14.3‑cp27‑none‑win_amd64.whl',
                           'cp27-windows-none': 'https://download.lfd.uci.edu/pythonlibs/archived/quickfix‑1.14.3‑cp27‑none‑win32.whl'
}


installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed
missingList = list(missing)
if missingList:
    for i in range(len(missingList)):
        if missingList[i] == 'configparser':
            # implement pip as a subprocess:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'configparser'])
        elif missingList[i] == 'pytest':
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pytest'])
        elif missingList[i] == 'quickfix':
            osname = platform.system().lower()
            if 'linux' in osname:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'quicktest'])
            elif 'windows' in osname:
                pythonVersionTuple = platform.python_version_tuple()
                pythonVersionShort = pythonVersionTuple[0] + pythonVersionTuple[1]
                platformMachine = platform.machine().lower()
                pipwheelkey = "cp" + pythonVersionTuple + "-" + osname + "-" + platformMachine
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', quickfix_windows_wheels[pipwheelkey]])
            else:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'quicktest'])


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
   install_requires=['wheel', 'configparser', 'pytest'], #external packages as dependencies
   scripts=[
            'scripts/cool',
            'scripts/skype',
           ]
)