''' 
GenieTelemetry CpuUtilizationCheck Plugin for NXOS
'''

from ..plugin import Plugin as BasePlugin


class Plugin(BasePlugin):
    
    def parse_args(self, argv):
        return WARNING('NXOS not supported CpuUtilizationCheck')
