''' 
GenieMonitor Traceback Check Plugin for IOSXE.
'''

# GenieMonitor
from ..plugin import Plugin as BasePlugin


class Plugin(BasePlugin):

    show_cmd = 'show logging'
    clear_cmd = 'clear logging'
