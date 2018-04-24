''' 
GenieTelemetry CpuUtilizationCheck Plugin for IOSXE
'''

from ..plugin import Plugin as BasePlugin

# parser
from parser.iosxe.show_platform import ShowProcessesCpuSorted

class Plugin(BasePlugin):

	PARSER_MODULE = ShowProcessesCpuSorted
