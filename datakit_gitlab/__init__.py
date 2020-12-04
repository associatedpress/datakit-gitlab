# -*- coding: utf-8 -*-

__author__ = """Serdar Tumgoren"""
__email__ = 'stumgoren@ap.org'
__version__ = '0.4.0'

from .commands.integrate import Integrate
from .commands import issues

# Squelch the horrifically verbose SSL warnings
import requests
requests.packages.urllib3.disable_warnings()
