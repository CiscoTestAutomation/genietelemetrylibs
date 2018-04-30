''' 
GenieTelemetry Traceback Check Plugin for IOSXE.
'''

# genie.telemetry
from ..plugin import Plugin as BasePlugin

from ats.utils import parser as argparse
from ats.datastructures import classproperty

class Plugin(BasePlugin):

    show_cmd = 'show logging'
    clear_cmd = 'clear logging'
    