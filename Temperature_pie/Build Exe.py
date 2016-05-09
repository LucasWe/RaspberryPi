from py2exe.build_exe import py2exe
from distutils.core import setup
import sys
from paramiko import transport
import paramiko


sys.argv.append("py2exe")
setup(console=["C:\Users\Lucas\PycharmProjects\Temperature_pie\ShowRoomtTemperature"])