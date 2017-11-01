'''
GenieMonitor KeepAlive Plugin.
'''

# GenieMonitor
from geniemonitor.plugins.bases import BasePlugin

class Plugin(BasePlugin):

    __plugin_name__ = 'KeepAlive Plugin'

    parser = None