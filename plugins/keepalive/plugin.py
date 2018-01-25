'''
GenieTelemetry KeepAlive Plugin.
'''

# GenieTelemetry
from genietelemetry.plugins.bases import BasePlugin

class Plugin(BasePlugin):

    __plugin_name__ = 'KeepAlive Plugin'

    parser = None