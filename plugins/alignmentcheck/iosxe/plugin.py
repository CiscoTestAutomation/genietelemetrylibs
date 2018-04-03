''' 
GenieMonitor Traceback Check Plugin for IOSXE.
'''

# GenieMonitor
from ..plugin import Plugin as BasePlugin

from ats.utils import parser as argparse
from ats.datastructures import classproperty

class Plugin(BasePlugin):

    show_cmd = 'show alignment'
