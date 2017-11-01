''' 
GenieMonitor KeepAlive Plugin for NXOS.
'''
import logging

# GenieMonitor
from ..plugin import Plugin as BasePlugin
from geniemonitor.results import OK

# module logger
logger = logging.getLogger(__name__)

class Plugin(BasePlugin):

    def execution(self, device, datetime):

        device.execute('\x0D', timeout=self.interval)
        return OK