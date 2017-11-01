''' 
GenieMonitor Traceback Check Plugin for NXOS.
'''

# GenieMonitor
from ..plugin import Plugin as BasePlugin


class Plugin(BasePlugin):

    show_cmd = 'show logging logfile'
    clear_cmd = 'clear logging logfile'
