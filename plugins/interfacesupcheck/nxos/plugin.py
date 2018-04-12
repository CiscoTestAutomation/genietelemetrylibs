''' 
GenieTelemetry Crashdumps Plugin for NXOS
'''

# GenieTelemetry
from ..plugin import Plugin as BasePlugin

# parser
from parser.nxos.show_interface import ShowInterfaceBrief


class Plugin(BasePlugin):

	PARSER_MODULE = ShowInterfaceBrief
