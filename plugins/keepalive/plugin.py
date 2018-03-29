'''
GenieTelemetry KeepAlive Plugin.
'''

# GenieTelemetry
from genie.telemetry.plugin import BasePlugin

class Plugin(BasePlugin):

    __plugin_name__ = 'KeepAlive Plugin'

    parser = None