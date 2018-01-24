''' 
GenieTelemetry KeepAlive Plugin for NXOS.
'''
import logging

# GenieTelemetry
from ..plugin import Plugin as BasePlugin
from genietelemetry.results import OK

# module logger
logger = logging.getLogger(__name__)

class Plugin(BasePlugin):

    def execution(self, device, datetime):

        device.execute('\x0D', timeout=self.interval)
        return OK