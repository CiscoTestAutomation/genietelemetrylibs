''' 
GenieTelemetry Alignment Check Plugin for IOSXR.
'''

from ..plugin import Plugin as BasePlugin


class Plugin(BasePlugin):
    
    def parse_args(self, argv):
        return WARNING('IOSXR not supported Alignment Check')