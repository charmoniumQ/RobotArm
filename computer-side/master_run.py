#!/usr/bin/python

from sys import path
from os.path import abspath
path.insert(0, abspath('.'))
from core import master

master.App.execute()
